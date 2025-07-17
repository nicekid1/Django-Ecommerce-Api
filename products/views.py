from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Value, CharField
from django.db.models.functions import Cast
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction


from .models import Product, Category , CartItem, OrderItem, Order
from .utils import send_request, verify_payment
from users.models import User
from .serializers import ProductSerializer, CategorySerializer, CartItemSerializer, OrderSerializer
from .filters import ProductFilter
from zeep import Client

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({'detail': 'No search query provided.'}, status=400)

        products = Product.objects.annotate(
            similarity=TrigramSimilarity(
                Cast('name', CharField()),
                Cast(Value(query), CharField())
            )
        ).filter(similarity__gt=0.2).order_by('-similarity')

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')
    
    def create(self, request, *args, **kwargs):
        user = request.user
        product = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product)
        except Product.DoesNotExist:
            return Response({'error': 'محصول یافت نشد.'}, status=404)

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def total(self, request):
        cart_items = self.get_queryset()
        total = sum(item.total_price for item in cart_items)
        return Response({'total_price': total})
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_user_cart(self, request, user_id=None):
        user = get_object_or_404(User, pk=user_id)
        if request.user != user and not request.user.is_staff:
            return Response({'detail': ' you have not access '}, status=status.HTTP_403_FORBIDDEN)
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
    
    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        if not cart_items:
            raise serializers.ValidationError("cart is empty")
        total = sum(item.product.price * item.quantity for item in cart_items)
        order = serializer.save(user=user, total_price=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart_items.delete()

ZARINPAL_REQUEST_URL = 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl'
ZARINPAL_START_PAY = 'https://sandbox.zarinpal.com/pg/StartPay/'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def start_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=404)

    callback_url = f"http://127.0.0.1:8000/api/store/payment/verify/{order.id}/"

    result = send_request(
        amount=int(order.total_price),
        description=f"Payment for Order #{order.id}",
        callback_url=callback_url,
        phone='09120000000' 
    )
    if result['status']:
        order.authority = result['authority']
        order.save()
        return redirect(result['url'])
    else:
        return Response({'error': f"Payment request failed: {result['code']}"}, status=400)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def verify_payment_view(request, order_id):
    authority = request.GET.get('Authority')
    if not authority or len(authority) != 36:
        return Response({'error': f'Invalid authority: {authority}'}, status=400)
    status = request.GET.get('Status')
    try:
        order = Order.objects.get(id=order_id, authority=authority)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=404)

    if status != 'OK':
        return Response({'error': 'Payment was canceled by user.'}, status=400)

    result = verify_payment(amount=int(order.total_price), authority=authority)

    if result['status']:
        order.status = 'processing'
        order.save()
        return Response({'message': 'Payment successful.', 'ref_id': result['RefID']})
    else:
        return Response({'error': f"Payment failed. Code: {result.get('code')} - {result.get('message')}"}, status=400)
