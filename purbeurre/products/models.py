from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)  # unique=True
    nutriscore = models.CharField(max_length=1, null=False)

    image = models.URLField(null=True)
    code = models.CharField(max_length=50)  # null=False
    stores = models.CharField(max_length=200)  # null=False
    url = models.URLField(unique=True)

    def __str__(self):
        return f"{self.name} {self.nutriscore}"


class Category(models.Model):
    name = models.CharField(max_length=100)  # unique=True
    # products = models.ManyToManyField(Product, through='Categorized')

    def __str__(self):
        return f"{self.name}"


class Categorized(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, verbose_name="product_id"
    )
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, verbose_name="category_id"
    )

    def __str__(self):
        return f"{self.product_id.name} {self.category_id.name}"
