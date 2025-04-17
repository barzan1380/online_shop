from django.shortcuts import render
from .forms import *
from cart.cart import Cart
from .models import *


# Create your views here.

def order_creation(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.save()

            for item in cart:

                OrderItem.objects.create(
                    order=order,
                    quantity=item['quantity'],
                    price=item['price'],
                    product=item['product'],
                )

            cart.clear()
            return render(request, 'order_created.html', {'order': order})

    else:
        form = OrderForm()
    return render(request, 'order_create.html', {'form': form})
