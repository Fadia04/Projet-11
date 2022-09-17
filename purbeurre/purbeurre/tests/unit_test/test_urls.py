import pytest
from django.urls import reverse, resolve
from django.test import Client
from favoris.models import Favorite
from products.models import Product, Category, Categorized
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User


def test_login_page_url():
    path = reverse("login")
    assert path == "/login/"
    assert resolve(path).view_name == "login"


def test_logout_user_url():
    path = reverse("logout")
    assert path == "/logout/"
    assert resolve(path).view_name == "logout"


def test_home_url():
    path = reverse("home")
    assert path == "/"
    assert resolve(path).view_name == "home"


def test_signup_page_url():
    path = reverse("signup")
    assert path == "/signup/"
    assert resolve(path).view_name == "signup"
    
  
def test_profile_page_url():
    path = reverse("profile")
    assert path == "/profile/"
    assert resolve(path).view_name == "profile"    


def test_favoris_page_url():
    path = reverse("favoris_page")
    assert path == "/favoris/"
    assert resolve(path).view_name == "favoris_page"


def test_results_url():
    path = reverse("results")
    assert path == "/results/"
    assert resolve(path).view_name == "results"


@pytest.mark.django_db
def test_favoris_url():
    Product.objects.create(name="nutella")
    path = reverse("favoris", kwargs={"id": 1})
    assert path == "/favoris/1/"
    assert resolve(path).view_name == "favoris"


@pytest.mark.django_db
def test_delete_favoris_url():
    prod = Product.objects.create(name="nutella")
    test_user = User.objects.create_user(username="test_user")
    Favorite.objects.create(product=prod, user=test_user)
    path = reverse("delete_favoris", kwargs={"id": 1})
    assert path == "/delete/1/"
    assert resolve(path).view_name == "delete_favoris"


@pytest.mark.django_db
def test_product_detail_url():
    Product.objects.create(name="nutella")
    path = reverse("product_detail", kwargs={"id": 1})
    assert path == "/products/1/"
    assert resolve(path).view_name == "product_detail"







