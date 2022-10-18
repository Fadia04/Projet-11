import pytest
from django.urls import reverse
from django.test import Client
from favoris.models import Favorite
from products.models import Product
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_integration_favoris():
    client = Client()
    prod = Product.objects.create(name="nutella")
    User.objects.create_user(username="test_user", password="123456789")
    client.login(username="test_user", password="123456789")
    path = reverse("favoris", kwargs={"id": prod.id})
    response = client.get(path)
    path = reverse("delete_favoris", kwargs={"id": response.context["favorite"][0].id})
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == "/favoris/"
    assert response.context == None


@pytest.mark.django_db
def test_integration_signup_login():
    client = Client()
    response = client.post(
        reverse("signup"),
        {
            "first_name": "Loulou",
            "last_name": "lili",
            "username": "test",
            "password1": "nanou1234",
            "password2": "nanou1234",
        },
    )
    path = reverse("login")
    response = client.post(path, {"username": "test", "password": "nanou1234"})
    assert response.status_code == 302
    assert response.url == "/"


@pytest.mark.django_db
def test_integration_login_logout():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("login")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    assert response.status_code == 302
    assert response.url == "/"
    path = reverse("logout")
    response = client.get(path)
    assert response.status_code == 302
    assert response.url == "/login/"


@pytest.mark.django_db
def test_integration_login_results():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("login")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    path = reverse("results")
    nutella_products = Product.objects.create(name="nutella1")
    response = client.post(path, {"query": "nutella"})
    assert response.status_code == 200
    assertTemplateUsed(response, "products/results.html")
    assert response.context["products"][0] == nutella_products


@pytest.mark.django_db
def test_integration_results_favoris():
    client = Client()
    product = Product.objects.create(name="nutella")
    path = reverse("results")
    response = client.post(path, {"query": "nutella"})
    Product.objects.all()
    User.objects.create_user(username="test_user", password="123456789")
    client.login(username="test_user", password="123456789")
    path = reverse("favoris", kwargs={"id": product.id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/favoris.html")
    expected_favoris = Favorite.objects.filter(product=product.id)
    assert response.context["favorite"][0] == expected_favoris[0]


@pytest.mark.django_db
def test_integration_login_favoris():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("login")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    product = Product.objects.create(name="nutella")
    path = reverse("favoris", kwargs={"id": product.id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/favoris.html")
    expected_favoris = Favorite.objects.filter(product=product.id)
    assert response.context["favorite"][0] == expected_favoris[0]
