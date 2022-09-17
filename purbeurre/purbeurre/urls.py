"""purbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import users.views
import products.views
import favoris.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", users.views.login_page, name="login"),
    path("logout/", users.views.logout_user, name="logout"),
    path("", products.views.home, name="home"),
    path("signup/", users.views.signup_page, name="signup"),
    path("profile/", users.views.profile_page, name="profile"),
    path("products/<int:id>/", products.views.product_detail, name="product_detail"),
    path("results/", products.views.results, name="results"),
    path("favoris/<int:id>/", favoris.views.favoris, name="favoris"),
    path("delete/<int:id>/", favoris.views.delete_favoris, name="delete_favoris"),
    path("favoris/", favoris.views.favoris, name="favoris_page"),
    path("legal_notices/", users.views.legal_notices, name="notices"),
]
