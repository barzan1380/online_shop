from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from shop.models import Product


# Create your views here.

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


def remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))


def cart_remove(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))


def decrease_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product)
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))
