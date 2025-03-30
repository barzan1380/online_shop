from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator


# Create your views here.


def product_list(request, category_slug=None):
    products = Product.objects.all()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    paginator = Paginator(products, 2)
    page_numer = request.GET.get('page')
    products_page = paginator.get_page(page_numer)

    context = {
        'products': products_page,
        'selected_category': selected_category
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})
