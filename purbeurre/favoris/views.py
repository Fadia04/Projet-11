from django.shortcuts import render, redirect
from favoris.models import Favorite
from products.models import Product
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def favoris(request, id=None):
    """View allowed to add a product in favoris page"""
    if id is not None:
        favoris = Product.objects.get(id=id)
        Favorite.objects.get_or_create(product=favoris, user=request.user)

    favorite = Favorite.objects.filter(user=request.user)

    return render(request, "products/favoris.html", {"favorite": favorite})


@login_required
def delete_favoris(request, id):
    """View allowed to delete a product saved by the user"""
    favoris = Favorite.objects.get(id=id)
    favoris.delete()
    return redirect("favoris_page")
