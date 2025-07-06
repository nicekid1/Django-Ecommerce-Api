from rest_framework import viewsets,permissions
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]
  