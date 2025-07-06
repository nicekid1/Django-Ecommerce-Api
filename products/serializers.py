from rest_framework import serializers
from .models import Product,Category,ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductImage
    fields = ['id','image']

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model:Category
    fields = ['id', 'name', 'parent']

class ProductSerializer(serializers.ModelSerializer):
  images = ProductImageSerializer(many=True, read_only=True)
  class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'brand',
            'color', 'size', 'weight', 'category', 'created_at', 'images'
        ]