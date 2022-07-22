from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from products.models import Product, Category
from favoris.models import Favorite
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
@login_required
def home(request):
    return render(request, 'products/home.html')
    
#def home(request):
    #template = loader.get_template('products/home.html')
    #return HttpResponse(template.render(request=request))
    
def product(request):
    products = Product.objects.all()
    return render(request, 'products/product.html', {'products' : products})

def product_detail(request,id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_detail.html', {'product': product})

def favoris(request,id):
    if request.method == "POST":
        favoris = Product.objects.get(id=id)
        Favorite.objects.get_or_create(product = favoris, user = request.user)
    favorite = Favorite.objects.filter(user = request.user)
    
    return render(request, 'products/favoris.html', {'favorite': favorite})
    
def results(request):
    if request.method == "POST":
        query = request.POST['query']
        #products = Product.objects.filter(Q(name__icontains=query) |
                                          #Q(product__name__icontains=query))
        
        products = Product.objects.filter(name__icontains=query).order_by('nutriscore')[:6]   
        #products = Product.objects.all()
        return render(request, 'products/results.html', {'query': query, 'products': products})
    else:
        message = "Nous n'avons pas trouvé le produit recherché" 
        return render(request, 'products/results.html', {'message': message}) 
   
#def search(request):
    #query = request.GET.get('query')
    #products = Product.objects.filter(name_icontains=query)
    #if not products.exists():
        #products = Product.objects.filter(categories_name_icontains=query)
     
    #if not products.exists():
         #message = "Nous n'avons trouvé aucun résultat"
    #else:
        #products = ["<li>{}</li>".format(product.name) for product in products]
        #message = """
            #Nous avons trouvé les produits correspondant à votre requête ! Les voici :
            #<ul>{}</ul>
        #""".format("</li><li>".join(products))
    #return render(request, 'products/product.html', {'products' : products})
