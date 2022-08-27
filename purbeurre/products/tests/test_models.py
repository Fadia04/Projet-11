"""
import pytest

from django.test import Client
from products.models import Product, Category, Categorized


@pytest.mark.django_db  
def test_product_model():
    client = Client()
    products = Product.objects.create(
               name = "nutella",
               nutriscore = "d")
    expected_value = "nutella d"
    assert str(products) == expected_value
    
@pytest.mark.django_db  
def test_category_model():
    client = Client()
    categories = Category.objects.create(
               name = "chocolat")
    expected_value = "chocolat"
    assert str(categories) == expected_value
    
@pytest.mark.django_db  
def test_categorized_model():
    client = Client()
    categorized = Categorized.objects.create(
               product_id = 20,
               category_id = 2)
    expected_value = "20 2"
    assert str(categorized) == expected_value
    """