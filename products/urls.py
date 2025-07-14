from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet,CartViewSet,OrderViewSet

router = DefaultRouter()
router.register('products',ProductViewSet, basename='products')
router.register('categories',CategoryViewSet,basename='categories')
router.register('cart',CartViewSet,basename='cart')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('',include(router.urls))
]
