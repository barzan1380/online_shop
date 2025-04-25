from django.shortcuts import render, redirect
import json
from django.contrib import messages
from account.models import CustomUser
import random
from django.contrib.auth import login
from datetime import datetime, timedelta
from .forms import *
from cart.cart import Cart
from .models import *


# Create your views here.

def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('order:order_creation')
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if CustomUser.objects.filter(phone=phone).exists():
                messages.error(request, 'this phone is registered')
                return redirect('order:verify_phone')
            else:
                token = ''.join(random.choices('0123456789', k=6))
                expiry_time = datetime.now() + timedelta(minutes=1)
                request.session['tokens'] = {'token': token, 'expires_at': expiry_time.isoformat(),
                                             'phone': phone}
                # send message
                messages.success(request, 'verification code sent successfully')
                return redirect('order:verify_code')
    else:
        form = PhoneVerificationForm()
    return render(request, 'verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        otp_data = request.session['tokens']
        code = request.POST['code']
        expires_at = datetime.fromisoformat(otp_data['expires_at'])
        verification_code = otp_data['token']
        phone = otp_data['phone']
        if datetime.now() < expires_at:
            if code == verification_code:
                user = CustomUser.objects.create_user(phone=phone)
                user.set_password('123456')
                user.save()
                # send sms
                login(request, user)
                del request.session['tokens']
                return redirect('order:order_creation')
            else:
                messages.error(request, 'verification_code is incorrect')
        else:
            messages.error(request, 'verification_code is timeout')
    return render(request, 'verify_code.html')


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


# # ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# CallbackURL = 'http://127.0.0.1:8000/orders/verify/'
#
#
# def send_request(request):
#     order = Oreder.objects.get(id=request.session['order_id'])
#     description = ""
#     for item in order.items.all():
#         description += item.product.name + ", "
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": order.get_final_cost(),
#         "Description": description,
#         "Phone": request.user.phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#         if response.status_code == 200:
#             response_json = response.json()
#             authority = response_json['Authority']
#             if response_json['Status'] == 100:
#                 return redirect(ZP_API_STARTPAY + authority)
#             else:
#                 return HttpResponse('Error')
#         return HttpResponse('response failed')
#     except requests.exceptions.Timeout:
#         return HttpResponse('Timeout Error')
#     except requests.exceptions.ConnectionError:
#         return HttpResponse('Connection Error')
#
#
# def verify(request):
#     order = Oreder.objects.get(id=request.session['order_id'])
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": order.get_final_cost(),
#         "Authority": request.Get.get('Authority'),
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#         if response.status_code == 200:
#             response_json = response.json()
#             reference_id = response_json['RefID']
#             if response_json['Status'] == 100:
#                 order.paid = True
#                 for item in order.items.all():
#                     item.product.inventory -= item.quantity
#                     item.product.save()
#                 order.save()
#                 return HttpResponse(f'successful , RefID: {reference_id}')
#             else:
#                 return HttpResponse('Error')
#         del request.session['order_id']
#         return HttpResponse('response failed')
#     except requests.exceptions.Timeout:
#         return HttpResponse('Timeout Error')
#     except requests.exceptions.ConnectionError:
#         return HttpResponse('Connection Error')