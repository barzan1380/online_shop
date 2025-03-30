from django.shortcuts import render, redirect
from functools import wraps


def seller_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'seller':
            return view_func(request, *args, **kwargs)
        return redirect("shop:products_list")

    return wrapper

