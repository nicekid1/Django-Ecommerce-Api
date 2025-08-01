from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,RegisterViewSet
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

router = DefaultRouter()
router.register('register',RegisterViewSet,basename='register')
router.register('profile',UserViewSet,basename='profile')

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include(router.urls))
]
