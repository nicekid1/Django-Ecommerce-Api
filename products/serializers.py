from rest_framework import serializers
from .models import Product,Category,ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProductImage
    fields = ['id','image']