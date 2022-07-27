from django.shortcuts import render, redirect
from favoris.models import Favorite
from products.models import Product

# Create your views here.
def favoris(request,id=None):
    if id is not None:
        favoris = Product.objects.get(id=id)
        Favorite.objects.get_or_create(product = favoris, user = request.user)
     
    favorite =Favorite.objects.filter(user = request.user)
    print(favorite)
    
    return render(request, 'products/favoris.html', {'favorite': favorite})

def delete_favoris(request, id):
    #favoris = Product.objects.get(id=id)
    #favoris = Favorite.objects.filter(id=id)
    favoris = Favorite.objects.filter(user = request.user)
    if request.method == 'POST':
        favoris.delete()
        return redirect('products/results.html')
    return render(request, 'favoris/delete.html', {'favoris': favoris})
    