from rest_framework import viewsets, permissions , filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product,Category,ProductImage
from .serializers import ProductSerializer,CategorySerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class ProductViewSet(viewsets.ModelViewSet):
  queryset=Product.objects.all().order_by('-created_at')
  serializer_class = ProductSerializer
  permission_classes = [IsAdminOrReadOnly]

  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_fields = ['category', 'color', 'size', 'brand']
  search_fields = ['name', 'brand']
  ordering_fields = ['price', 'created_at']

class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAdminOrReadOnly]
