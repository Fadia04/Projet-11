from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.
    
class Favorite(models.Model):           
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='product')
    #substitut = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='substitut')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    