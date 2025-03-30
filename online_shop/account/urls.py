from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
]
