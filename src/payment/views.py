from django.shortcuts import render
from django.http import JsonResponse
from cart.cart import Cart

from .models import ShippingAddress, Order, OrderItem

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


def complete_order(request):
    if request.POST.get("action") == "post":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")

        # all in one shipping address

        shipping_address = (
            address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode
        )
        cart = Cart(request)
        # get the total price of the items in the cart
        total_cost = cart.get_total()

        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user,
            )

            # order_id = order.pk
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["price"],
                    user=request.user,
                )

        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
            )

            # order_id = order.pk
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["price"],
                )
        order_success = True
        return JsonResponse({"success": order_success})


def payment_success(request):
    # clear shopping cart

    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    return render(request, "payment/payment_success.html")


def payment_failed(request):
    return render(request, "payment/payment_failed.html")
