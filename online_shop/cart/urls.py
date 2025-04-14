from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # path('decrease/<int:product_id>/', views.decrease_from_cart, name='decrease_from_cart'),
    path('detail/', cart_detail, name='cart_detail'),
    path('remove/<int:product_id>', remove, name='remove'),
    path('cart_remove/', cart_remove, name='cart_remove'),
    path('decrease_from_cart/<int:product_id>/', decrease_from_cart, name='decrease_from_cart'),
]
