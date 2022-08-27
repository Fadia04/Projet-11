from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from products.models import Product, Category, Categorized
from favoris.models import Favorite
from django.db.models import Q
from django.core.paginator import Paginator

from itertools import chain
# Create your views here.

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


    
def results(request):
    if request.method == "POST":
        query = request.POST['query']
        #products = Product.objects.filter(Q(name__icontains=query) |
                                          #Q(product__name__icontains=query))
        
        products = Product.objects.filter(name__icontains=query).order_by('nutriscore')[:9]   
        #Recherche de la listes des id de produit à l'aide de la tablea categorized
        #categories = Category.objects.get(name__icontains=query).order_by('nutriscore')[:3]
        #categorized=Categorized.objects.filter(category_id = categories.id, product_id = products.id)
        #products_pk = []
        
        #for category_id in categorized:
            #products_pk.append(category_id)
        #products_filter = Product.objects.filter(pk__in=products_pk).order_by('nutriscore')[:3]
        #all_products = chain(products, products_filter)
        return render(request, 'products/results.html', {'query': query, 'products': products})
    else:
        message = "Nous n'avons pas trouvé le produit recherché" 
        return render(request, 'products/results.html', {'message': message}) 
   
#def search(request):
    #query = request.GET.get('query')
    #products = Product.objects.filter(name_icontains=query)
    #if products.nutriscore!= a:
        #products = Category.objects.filter(name_icontains=query)
     
    #if not products.exists():
         #message = "Nous n'avons trouvé aucun résultat"
    #else:
        #products = ["<li>{}</li>".format(product.name) for product in products]
        #message = """
            #Nous avons trouvé les produits correspondant à votre requête ! Les voici :
            #<ul>{}</ul>
        #""".format("</li><li>".join(products))
    #return render(request, 'products/product.html', {'products' : products})
