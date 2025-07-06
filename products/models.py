from django.db import models

class Category(models.Model):
  name =models.CharField(max_length=100)
  parent = models.models.ForeignKey("self", null=True,blank=True, on_delete=models.CASCADE,related_name='children')
  def __str__(self):
    return self.name