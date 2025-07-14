from rest_framework import serializers
from .models import Product,Category,ProductImage,CartItem

class ProductImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductImage
    fields = ['id','image']

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name', 'parent']

class ProductSerializer(serializers.ModelSerializer):
  images = ProductImageSerializer(many=True, read_only=True)
  class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'brand',
            'color', 'size', 'weight', 'category', 'created_at', 'images'
        ]

class CartItemSerializer(serializers.ModelSerializer):
  product_detail = ProductSerializer(source = 'product', read_only=True)
  total_price = serializers.SerializerMethodField()
  
  class Meta:
    model = CartItem
    fields = ['id', 'product', 'product_detail', 'quantity', 'total_price']

  
  def get_total_price(self, obj):
    if isinstance(obj, dict):
      product = obj['product']
      quantity = obj['quantity']
      price = product.price
      return price * quantity
    return obj.product.price * obj.quantity

    