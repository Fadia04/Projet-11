from django.db import models


# Create your models here.


class Product(models.Model):
    """Model for the products with required parameters"""

    name = models.CharField(max_length=512)  # unique=True
    nutriscore = models.CharField(max_length=1, null=False)
    image = models.URLField(null=True)
    code = models.CharField(max_length=512)  # null=False
    stores = models.CharField(max_length=512)  # null=False
    url = models.URLField(unique=True)

    def __str__(self):
        return f"{self.name} {self.nutriscore}"


class Category(models.Model):
    """Model for the categories"""

    name = models.CharField(max_length=512)  # unique=True

    def __str__(self):
        return f"{self.name}"


class Categorized(models.Model):
    """Model for the associative table with required fields"""

    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, verbose_name="product_id"
    )
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, verbose_name="category_id"
    )

    def __str__(self):
        return f"{self.product_id.name} {self.category_id.name}"


class Comment(models.Model):
    product = models.ForeignKey(
        Product, related_name="comments", on_delete=models.CASCADE
    )
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} {self.commenter_name}"
