from rest_framework import viewsets,permissions
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]
  def get_queryset(self):
    return User.objects.filter(id=self.request.user.id)

class RegisterViewSet(viewsets.ModelViewSet):
  queryset = User.objects.none()
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny]

  def list(self,request):
    return Response({'detail': 'Not allowed'}, status=405)
