from django.urls import path
from .views import seller_dashboard

app_name = 'seller'

urlpatterns = [
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard')
]
