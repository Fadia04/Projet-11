import pytest
from django.urls import reverse, resolve
from django.test import Client
from favoris.models import Favorite
from products.models import Product, Category, Categorized
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User



@pytest.mark.django_db
def test_login_page_view():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("login")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    assert response.status_code == 302
    assert response.url == "/"


@pytest.mark.django_db
def test_logout_page_view():
    client = Client()
    path = reverse("logout")
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == "/login/"


@pytest.mark.django_db
def test_signup_page_view():
    client = Client()
    test_user = {
        "first_name": "Loulou",
        "last_name": "lili",
        "username": "test",
        "password1": "nanou1234",
        "password2": "nanou1234",
    }
    path = reverse("signup")
    response = client.post(path, test_user)
    assert response.status_code == 302
    assert response.url == "/login/"


def test_home_view():
    client = Client()
    client.post("/")
    path = reverse("home")
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/home.html")


@pytest.mark.django_db
def test_product_detail_view(reset_sequences=True, transaction=True):
    client = Client()
    product = Product.objects.create(name="nutella")
    path = reverse("product_detail", kwargs={"id": product.id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/product_detail.html")
    assert response.context["product"] == product


@pytest.mark.django_db
def test_results_view():
    client = Client()
    prods = "nutella1", "nutella2", "nutella3"
    product1 = Product.objects.create(name="nutella1", url="1")
    product2 = Product.objects.create(name="nutella2", url="2")
    product3 = Product.objects.create(name="nutella3", url="3")
    path = reverse("results")
    response = client.post(path, {"query": "nutella"})
    nutella_products = Product.objects.all()
    assert response.status_code == 200
    assertTemplateUsed(response, "products/results.html")
    assert response.context["products"][0] == nutella_products[0]
    assert response.context["products"][1] == nutella_products[1]
    assert response.context["products"][2] == nutella_products[2]


@pytest.mark.django_db
def test_favoris_view():
    client = Client()
    prod = Product.objects.create(name="nutella")
    test_user = User.objects.create_user(username="test_user", password="123456789")
    client.login(username="test_user", password="123456789")
    path = reverse("favoris", kwargs={"id": prod.id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/favoris.html")
    expected_favoris = Favorite.objects.filter(product=prod.id)
    assert response.context["favorite"][0] == expected_favoris[0]


@pytest.mark.django_db
def test_favoris_delete_view():
    client = Client()
    prod = Product.objects.create(name="nutella")
    test_user = User.objects.create_user(username="test_user", password="123456789")
    client.login(username="test_user", password="123456789")
    favorite = Favorite.objects.create(product=prod, user=test_user)
    path = reverse("delete_favoris", kwargs={"id": favorite.id})
    response = client.get(path)
    assert response.status_code == 302
    assert response.context == None
    assert response.url == "/favoris/"