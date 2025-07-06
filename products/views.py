from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.decorators import action
from django.db.models import Value, CharField
from django.db.models.functions import Cast
from rest_framework.response import Response

from .models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer
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
        similarity=TrigramSimilarity('name', Cast(Value(query), CharField()))
        ).filter(similarity__gt=0.2).order_by('-similarity')

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAdminOrReadOnly]
