import pytest

from django.urls import reverse, resolve
from django.test import Client
from favoris.models import Favorite
from products.models import Product, Category, Categorized
from pytest_django.asserts import assertTemplateUsed
from django.conf import settings
from django.contrib.auth.models import User
 
def test_login_page_url():
    path = reverse('login')
    assert path == "/login/"
    assert resolve(path).view_name == "login"
    
def test_logout_user_url():
    path = reverse('logout')
    assert path == "/logout/"
    assert resolve(path).view_name == "logout"
    
def test_home_url():
    path = reverse('home')
    assert path == "/"
    assert resolve(path).view_name == "home"
    
def test_signup_page_url():
    path = reverse('signup')
    assert path == "/signup/"
    assert resolve(path).view_name == "signup"
    

   
def test_favoris_page_url():    
    path = reverse('favoris_page')    
    assert path == "/favoris/"
    assert resolve(path).view_name == "favoris_page"
    
def test_products_url():    
    path = reverse('product')    
    assert path == "/products/"
    assert resolve(path).view_name == "product"
    
def test_results_url():    
    path = reverse('results')    
    assert path == "/results/"
    assert resolve(path).view_name == "results"
    
@pytest.mark.django_db    
def test_favoris_url():
    Product.objects.create(name='nutella')
    path = reverse('favoris', kwargs={'id':1})    
    assert path == "/favoris/1/"
    assert resolve(path).view_name == "favoris"
    
@pytest.mark.django_db    
def test_delete_favoris_url():
    prod = Product.objects.create(name = "nutella")
    test_user = User.objects.create_user(username = "test_user")
    Favorite.objects.create(product=prod, user=test_user)
    path = reverse('delete_favoris', kwargs={'id':1})    
    assert path == "/delete/1/"
    assert resolve(path).view_name == "delete_favoris"
    
@pytest.mark.django_db    
def test_product_detail_url():    
    Product.objects.create(name ='nutella')
    path = reverse('product_detail', kwargs={'id':1})    
    assert path == "/products/1/"
    assert resolve(path).view_name == "product_detail"
  
    
@pytest.mark.django_db  
def test_favoris_model():
    client = Client()
    prod = Product.objects.create(name = "nutella")
    test_user = User.objects.create_user(username = "test_user", password="123456789")
    favoris = Favorite.objects.create(product=prod, user=test_user)
    expected_value = "nutella test_user"
    assert str(favoris) == expected_value
    
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
    product = Product.objects.create(name="LU")
    category = Category.objects.create(name="biscuit")
    categorized = Categorized.objects.create(product_id=product, category_id=category)
    expected_value = "LU biscuit"
    assert str(categorized) == expected_value
    
@pytest.mark.django_db  
def test_login_page_view():
    client = Client()
    #client.post('/login/', {'username': 'loulou', 'password': 'kiki'})
    path = reverse('login')
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "users/login.html")
    
@pytest.mark.django_db  
def test_logout_page_view():
    client = Client()
    path = reverse('logout')
    response = client.get(path)
    assert response.status_code == 302
    #assertTemplateUsed(response, "users/login.html")
    
def test_signup_page_view():
    client = Client()
    client.post('/signup/')
    path = reverse('signup')
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "users/signup.html")

def test_home_view():
    client = Client()
    client.post('/')
    path = reverse('home')
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/home.html")

@pytest.mark.django_db    
def test_product_detail_view(reset_sequences=True, transaction=True):
    client = Client()
    product = Product.objects.create(name="nutella")
    print("Check ID : ", product.id)
    path = reverse('product_detail', kwargs={'id':product.id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/product_detail.html")
    assert response.context['product'] == product
    print(response.context)
       
@pytest.mark.django_db  
def test_results_view():
    client = Client()
    prods='nutella1', 'nutella2', 'nutella3'
    product1 = Product.objects.create(name="nutella1", url="1")
    product2 = Product.objects.create(name="nutella2", url="2")
    product3 = Product.objects.create(name="nutella3", url="3")
    
    path= reverse('results')
    response = client.post(path, {'query': 'nutella', 'products': prods})
    
    nutella_products = Product.objects.all()
    assert response.status_code == 200
    assertTemplateUsed(response, "products/results.html")
    assert response.context['products'][0] == nutella_products[0]
    assert response.context['products'][1] == nutella_products[1]
    assert response.context['products'][2] == nutella_products[2]
    
   
@pytest.mark.django_db  
def test_favoris_view():
    client = Client()
    prod=Product.objects.create(name='nutella')
    test_user = User.objects.create_user(username = "test_user", password="123456789")
    client.login(username = "test_user", password="123456789")
    path = reverse('favoris', kwargs={'id':prod.id})
    response = client.get(path)
    assert response.status_code == 200
    assertTemplateUsed(response, "products/favoris.html")
    expected_favoris = Favorite.objects.filter(product=prod.id)
    assert response.context['favorite'][0] == expected_favoris[0]
    
@pytest.mark.django_db  
def test_favoris_delete_view():
    client = Client()
    prod=Product.objects.create(name='nutella')
    test_user = User.objects.create_user(username = "test_user", password="123456789")
    client.login(username = "test_user", password="123456789")
    favorite = Favorite.objects.create(product=prod, user = test_user)

    path = reverse('delete_favoris', kwargs={'id':favorite.id})
    response = client.get(path)
    assert response.status_code == 302
    assert response.context ==None

@pytest.mark.django_db    
def test_integration_favoris():
    client = Client()
    prod=Product.objects.create(name='nutella')
    test_user = User.objects.create_user(username = "test_user", password="123456789")
    client.login(username = "test_user", password="123456789")
    path = reverse('favoris', kwargs={'id':prod.id})
    response = client.get(path)
    
    path = reverse('delete_favoris', kwargs={'id':response.context['favorite'][0].id})
    response = client.get(path)
    assert response.status_code == 302
    assert response.context ==None
    
    
    
    
    
    #Créer 3 produit qui contiennent le mot nutella
    #CRéer 2 autre produit qui n'ont rien à voir avec nutella
    # Tu fait ta requête post avec la query nutella
    #Créer une liste avec les 3 produit nutella nutella_prodcuts = [product1, produt2, produt3]
    #Check status code, check template et check contexte reponse.context['prodcuts'] == nutella_products, query == nutella
    