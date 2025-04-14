app_name = 'shop'
from django.urls import path
from .views import *

urlpatterns = [
    path('products/', product_list, name='products_list'),
    path('products/category/<slug:category_slug>/', product_list, name='products_list_by_category'),
    path('product/<int:pk>/<slug:slug>/', product_detail, name='product_detail'),
]
