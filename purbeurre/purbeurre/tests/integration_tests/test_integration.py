import pytest
from django.urls import reverse
from django.test import Client
from favoris.models import Favorite
from products.models import Product, Category, Categorized
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


@pytest.mark.django_db
def test_integration_login_results():
    client = Client()
    User.objects.create_user(username="test_user", password="123456789")
    path = reverse("login")
    response = client.post(path, {"username": "test_user", "password": "123456789"})
    path = reverse("results")
    prod1 = Product.objects.create(name="nutella", url="1")
    prod2 = Product.objects.create(name="pur beurre de cacahuetes", url="2")
    prod3 = Product.objects.create(name="evian", url="3")
    category1 = Category.objects.create(name="pates a tartiner")
    category2 = Category.objects.create(name="boissons")
    Categorized.objects.create(product_id=prod1, category_id=category1)
    Categorized.objects.create(product_id=prod2, category_id=category2)
    Categorized.objects.create(product_id=prod3, category_id=category1)
    response = client.post(path, {"query": "nutella"})
    assert response.status_code == 200
    assertTemplateUsed(response, "products/results.html")
    assert response.context["products"][0] == prod1
    assert response.context["products"][1] == prod3
