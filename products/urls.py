from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,CategoryViewSet,CartViewSet,OrderViewSet,start_payment,verify_payment_view

router = DefaultRouter()
router.register('products',ProductViewSet, basename='products')
router.register('categories',CategoryViewSet,basename='categories')
router.register('cart',CartViewSet,basename='cart')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('',include(router.urls))
]

urlpatterns += [
    path('payment/start/<int:order_id>/', start_payment, name='start_payment'),
    path('payment/verify/<int:order_id>/', verify_payment_view, name='verify_payment'),
]