
from asyncio.windows_events import NULL
from django.db import models
from django.conf import settings


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100) #unique=True
    nutriscore = models.CharField(max_length=1, null=False)
    #nutriscore = models.URLField(null=True)
    image = models.URLField(null=True)
    code = models.CharField(max_length=50)#null=False
    stores = models.CharField(max_length=200)#null=False
    url = models.URLField(unique=True)    
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100) #unique=True
    #products = models.ManyToManyField(Product, through='Categorized')
    
    def __str__(self):
        return self.name    

class Categorized(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, verbose_name='product_id')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name='category_id')
    
