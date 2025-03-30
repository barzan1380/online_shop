from django.shortcuts import render
from .decorators import seller_required


# Create your views here.

@seller_required
def seller_dashboard(request):
    return render(request, 'account/seller_dashboard.html')

