from django.shortcuts import render, redirect
from datetime import datetime
from products.models import Product,Categorized, Comment
from products.forms import CommentForm



def home(request):
    """View allowed to return home page"""
    return render(request, "products/home.html")


def product_detail(request, id):
    """View allowed to display products informations in detail page"""
    product = Product.objects.get(id=id)
    return render(request, "products/product_detail.html", {"product": product})


def results(request):
    """View allowed to get the user request filtered by name
    and get a list of products. Among those products, a list of products id and
    category id were returned with categorized class and finaly a list of 9
    corresponding products were displayed in result page"""
    if request.method == "POST":
        query = request.POST["query"]
        products = Product.objects.filter(name__icontains=query).order_by("nutriscore")[
            :50
        ]
        print(products)
        categorized = Categorized.objects.filter(product_id__in=products).order_by(
            "product_id"
        )[:10]
        all_categories = [category.category_id for category in categorized]
        categorized_product = Categorized.objects.filter(
            category_id__in=all_categories
        ).order_by("category_id")
        print(categorized_product)
        all_categorized_products = [
            category.product_id.id for category in categorized_product
        ]
        all_products = Product.objects.filter(id__in=all_categorized_products).order_by(
            "nutriscore"
        )[:9]

        return render(
            request, "products/results.html", {"query": query, "products": all_products}
        )
    else:
        message = "Nous n'avons pas trouvé le produit recherché, veuillez retaper votre demande"
        return render(request, "products/results.html", {"message": message})


def add_comment(request, id):
    """View allowed to add a user's comment in add-comment page and to save it """
    product = Product.objects.get(id=id)
    form = CommentForm(instance=product)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=product)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data["comment_body"]
            comments = Comment(
                product=product,
                commenter_name=name,
                comment_body=body,
                date_added=datetime.now(),
            )
            comments.save()
            return redirect("product_detail", id=id)
        else:
            print("form is not valid")
    else:
        form = CommentForm
    context = {"form": form}
    return render(request, "products/add_comment.html", context)


def delete_comment(request, id):
    """View to delete a comment by it's owner"""
    comment = Comment.objects.filter(product=id)
    comment.delete()
    return redirect("product_detail", id=id)
