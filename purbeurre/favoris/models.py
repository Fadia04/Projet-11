from django.db import models
from django.conf import settings
from products.models import Product


# Create your models here.


class Favorite(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name="product"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )

    def __str__(self):
        return f"{self.product.name} {self.user.username}"
