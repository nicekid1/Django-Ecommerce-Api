from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet

router = DefaultRouter()
router.register('products',ProductViewSet, basename='products')
router.register('categories',CategoryViewSet,basename='categories')

urlpatterns = [
    path('',include(router.urls))
]
