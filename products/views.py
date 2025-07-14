from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Value, CharField
from django.db.models.functions import Cast
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import get_object_or_404

from .models import Product, Category , CartItem
from users.models import User
from .serializers import ProductSerializer, CategorySerializer, CartItemSerializer
from .filters import ProductFilter


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
    
    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    @action(detail=False, methods=['get'])
    def total(self, request):
        cart_items = self.get_queryset()
        total = sum(item.total_price for item in cart_items)
        return Response({'total_price': total})
    
    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def get_user_cart(self, request, user_id=None):
        user = get_object_or_404(User,pk=user_id)
        if request.user != user and not request.user.is_staff:
            return Response({'detail': ' you have not access '}, status=status.HTTP_403_FORBIDDEN)
        cart_items = CartItem.objects.filter(user=user).select_related('product')
        serializer = self.get_serializer(cart_items,many=True)
        return Response(serializer.data)
