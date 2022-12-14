import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from django.test import Client
from favoris.models import Favorite
from products.models import Product, Category, Categorized
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
def test_favoris_view():
    client = Client()
    prod = Product.objects.create(name="nutella")
    User.objects.create_user(username="test_user", password="123456789")
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


@pytest.mark.django_db
def test_add_comment_view():
    client = Client()
    prod = Product.objects.create(name="coca cola zero")
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("add-comment", kwargs={"id": prod.id})
    data = {"comment_body": "CommentTextMessageTest"}
    response = client.post(path, data)
    assert response.status_code == 302
    path = reverse("product_detail", kwargs={"id": prod.id})
    assert response.url == path


@pytest.mark.django_db
def test_add_comment_with_wrong_data():
    client = Client()
    prod = Product.objects.create(name="coca cola zero")
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("add-comment", kwargs={"id": prod.id})
    data = {"comment_fake": "CommentTextMessageTest"}
    response = client.post(path, data)
    assert response.status_code == 200
    assertTemplateUsed("products/add_comment.html")


@pytest.mark.django_db
def test_add_comment_get_page():
    client = Client()
    prod = Product.objects.create(name="coca cola zero")
    User.objects.create_user(username="Lamia", password="lili5678")
    client.login(username="Lamia", password="lili5678")
    path = reverse("add-comment", kwargs={"id": prod.id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed("products/add_comment.html")


@pytest.mark.django_db
def test_results_view():
    client = Client()
    prod1 = Product.objects.create(name="nutella", url="1")
    prod2 = Product.objects.create(name="evian", url="2")
    prod3 = Product.objects.create(name="pur beurre de cacahuètes", url="3")
    category1 = Category.objects.create(name="pates a tartiner")
    category2 = Category.objects.create(name="boissons")

    Categorized.objects.create(product_id=prod1, category_id=category1)
    Categorized.objects.create(product_id=prod2, category_id=category2)
    Categorized.objects.create(product_id=prod3, category_id=category1)
    path = reverse("results")
    response = client.post(path, {"query": "nutella"})
    assert response.status_code == 200
    assertTemplateUsed(response, "products/results.html")
    assert response.context["products"][0] == prod1
    assert response.context["products"][1] == prod3 