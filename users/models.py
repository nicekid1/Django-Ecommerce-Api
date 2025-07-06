from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
  isAdmin = models.BooleanField(default=False)
  email_verified  = models.BooleanField(default=False)
