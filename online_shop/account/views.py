from django.shortcuts import render
from .decorators import admin_required


# Create your views here.

@admin_required
def admin_dashboard(request):
    return render(request, 'account/admin_dashboard.html')

