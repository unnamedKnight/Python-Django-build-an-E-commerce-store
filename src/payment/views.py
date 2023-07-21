from django.shortcuts import render
from .models import ShippingAddress

# Create your views here.


def checkout(request):
    if request.user.is_authenticated:
        try:
            shipping = ShippingAddress.objects.get(user=request.user)
            context = {"shipping": shipping}
            return render(request, "payment/checkout.html", context)
        except ShippingAddress.DoesNotExist:
            return render(request, "payment/checkout.html")
    return render(request, "payment/checkout.html")


def payment_success(request):
    return render(request, "payment/payment_success.html")


def payment_failed(request):
    return render(request, "payment/payment_failed.html")
