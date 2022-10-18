import pytest
from favoris.models import Favorite
from products.models import Product, Category, Categorized
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_favoris_model():
    prod = Product.objects.create(name="nutella")
    test_user = User.objects.create_user(username="test_user", password="123456789")
    favoris = Favorite.objects.create(product=prod, user=test_user)
    expected_value = "nutella test_user"
    assert str(favoris) == expected_value


@pytest.mark.django_db
def test_product_model():
    products = Product.objects.create(name="nutella", nutriscore="d")
    expected_value = "nutella d"
    assert str(products) == expected_value


@pytest.mark.django_db
def test_category_model():
    categories = Category.objects.create(name="chocolat")
    expected_value = "chocolat"
    assert str(categories) == expected_value


@pytest.mark.django_db
def test_categorized_model():
    product = Product.objects.create(name="LU")
    category = Category.objects.create(name="biscuit")
    categorized = Categorized.objects.create(product_id=product, category_id=category)
    expected_value = "LU biscuit"
    assert str(categorized) == expected_value
    