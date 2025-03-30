from django.contrib import admin
from .models import *
from django.utils import timezone

# Register your models here.

class ActiveDisccountFilter(admin.SimpleListFilter):
    title = 'وضعیت تخفیف'
    parameter_name = 'off'

    def lookups(self, request, model_admin):
        return [
            ('Yes', 'دارای تخفیف'),
            ('No', 'بدون تخفیف')
        ]

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'Yes':
            return queryset.filter(discount_start__lte=now, discount_end__gte=now, off__gt=0)
        elif self.value() == 'No':
            return queryset.exclude(discount_start__lte=now, discount_end__gte=now, off__gt=0)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'price', 'off', 'is_discount_active', 'get_final_price')
    list_filter = ('category',ActiveDisccountFilter)
    list_editable = ('off',)
    search_fields = ('name', 'description')

    def is_discount_active(self, obj):
        return obj.is_discount_active()

    is_discount_active.boolean = True
    is_discount_active.short_description = 'تخفیف فعال است؟'

    def get_final_price(self, obj):
        return f"{obj.get_final_price():,}"'تومان'

    get_final_price.short_description = 'قیمت پس از تخفیف'


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
