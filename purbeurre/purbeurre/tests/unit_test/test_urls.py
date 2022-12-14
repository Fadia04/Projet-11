import pytest
from django.urls import reverse, resolve
from favoris.models import Favorite
from products.models import Product
from django.contrib.auth.models import User


def test_login_page_url():
    """Test the login url"""
    path = reverse("login")
    assert path == "/login/"
    assert resolve(path).view_name == "login"


def test_logout_user_url():
    """Test the logout url"""
    path = reverse("logout")
    assert path == "/logout/"
    assert resolve(path).view_name == "logout"


def test_home_url():
    """Test the home url"""
    path = reverse("home")
    assert path == "/"
    assert resolve(path).view_name == "home"


def test_signup_page_url():
    """Test the signup url"""
    path = reverse("signup")
    assert path == "/signup/"
    assert resolve(path).view_name == "signup"


def test_profile_page_url():
    """Test the profile_page url"""
    path = reverse("profile")
    assert path == "/profile/"
    assert resolve(path).view_name == "profile"


def test_favoris_page_url():
    """Test the favoris_page url"""
    path = reverse("favoris_page")
    assert path == "/favoris/"
    assert resolve(path).view_name == "favoris_page"


def test_results_url():
    """test the result url"""
    path = reverse("results")
    assert path == "/results/"
    assert resolve(path).view_name == "results"


@pytest.mark.django_db
def test_favoris_url():
    """Test the favoris url"""
    Product.objects.create(name="nutella")
    path = reverse("favoris", kwargs={"id": 1})
    assert path == "/favoris/1/"
    assert resolve(path).view_name == "favoris"


@pytest.mark.django_db
def test_delete_favoris_url():
    """Test the delete_favoris url"""
    prod = Product.objects.create(name="nutella")
    test_user = User.objects.create_user(username="test_user")
    Favorite.objects.create(product=prod, user=test_user)
    path = reverse("delete_favoris", kwargs={"id": 1})
    assert path == "/delete/1/"
    assert resolve(path).view_name == "delete_favoris"


@pytest.mark.django_db
def test_product_detail_url():
    """Test the product_detail url"""
    Product.objects.create(name="nutella")
    path = reverse("product_detail", kwargs={"id": 1})
    assert path == "/products/1/"
    assert resolve(path).view_name == "product_detail"


@pytest.mark.django_db
def test_add_comment_url():
    """Test the add_comment url"""
    Product.objects.create(name="nutella")
    path = reverse("add-comment", kwargs={"id": 1})
    assert path == "/products/1/add-comment"
    assert resolve(path).view_name == "add-comment"


@pytest.mark.django_db
def test_delete_comment_url():
    """Test the delete_comment url"""
    Product.objects.create(name="nutella")
    path = reverse("delete-comment", kwargs={"id": 1})
    assert path == "/products/1/delete-comment"
    assert resolve(path).view_name == "delete-comment"


def test_reset_password_url():
    """Test the rest_password url"""
    path = reverse("reset_password")
    assert path == "/reset_password"
    assert resolve(path).view_name == "reset_password"


def test_reset_password_send_url():
    path = reverse("password_reset_done")
    assert path == "/reset_password_send"
    assert resolve(path).view_name == "password_reset_done"


def test_password_reset_confirm_url():
    """Test the confirm of reset url"""
    path = reverse(
        "password_reset_confirm", kwargs={"uidb64": "uidb64", "token": "token"}
    )
    assert path == "/reset/uidb64/token"
    assert resolve(path).view_name == "password_reset_confirm"


def test_password_reset_complete_url():
    """Test the reset password url"""
    path = reverse("password_reset_complete")
    assert path == "/reset_password_complete"
    assert resolve(path).view_name == "password_reset_complete"
