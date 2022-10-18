from django.shortcuts import render
from products.models import Product


# Create your views here.


def home(request):
    """View allowed to return home page"""
    return render(request, "products/home.html")


def product_detail(request, id):
    """View allowed to display products informations in detail page"""
    product = Product.objects.get(id=id)
    return render(request, "products/product_detail.html", {"product": product})


def results(request):
    """View allowed to get the user request filtered by name 
    and displays a list of 6 products in results page"""
    if request.method == "POST":
        query = request.POST["query"]
        products = Product.objects.filter(name__icontains=query).order_by("nutriscore")[
            :6
        ]
        return render(
            request, "products/results.html", {"query": query, "products": products}
        )
    else:
        message = "Nous n'avons pas trouvé le produit recherché, veuillez retaper votre demande"
        return render(request, "products/results.html", {"message": message})

