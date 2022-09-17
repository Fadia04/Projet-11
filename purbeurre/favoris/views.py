from django.shortcuts import render, redirect
from favoris.models import Favorite
from products.models import Product
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def favoris(request, id=None):
    if id is not None:
        favoris = Product.objects.get(id=id)
        Favorite.objects.get_or_create(product=favoris, user=request.user)

    favorite = Favorite.objects.filter(user=request.user)

    return render(request, "products/favoris.html", {"favorite": favorite})


@login_required
def delete_favoris(request, id):
    favoris = Favorite.objects.get(id=id)
    favoris.delete()
    return redirect("favoris_page")
