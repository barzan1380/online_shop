from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('create/', order_creation, name='order_creation'),
    path('veryfi-code/', verify_code, name='verify_code'),
    path('veryfi-phone/', verify_phone, name='verify_phone'),
]
