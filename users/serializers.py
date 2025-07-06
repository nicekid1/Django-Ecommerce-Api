from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    field = ('username', 'email', 'password', 'password2')
  def validate(self,attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError({"password": "Passwords didn't match."})
    return attrs
  