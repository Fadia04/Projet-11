from django.contrib import admin
from products.models import Product
from products.models import Category
from products.models import Categorized


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Categorized)
