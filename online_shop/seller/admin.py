from django.contrib import admin
from .models import Seller

# Register your models here.


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name']
    search_fields = ['user__phone', 'store_name']
