from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator


# Create your views here.


def product_list(request, category_slug=None):
    products = Product.objects.all()
    selected_category = None
    sort_by = request.GET.get('sort_by')
    categories = Category.objects.all()
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    if sort_by == "created":
        products = products.order_by('-created')
    elif sort_by == "new_price":
        products = products.order_by('-price')
    elif sort_by == "price":
        products = products.order_by('price')
    elif sort_by == "created":
        products = products.order_by('created')

    paginator = Paginator(products, 2)
    page_numer = request.GET.get('page')
    products_page = paginator.get_page(page_numer)

    context = {
        'products': products_page,
        'selected_category': selected_category,
        'categories': categories
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})
