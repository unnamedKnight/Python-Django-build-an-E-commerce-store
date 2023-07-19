from django.shortcuts import render
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .cart import Cart

# Create your views here.


def cart_summary(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, "cart/cart_summary.html", context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))
        product = get_object_or_404(Product, pk=product_id)
        cart.add(product=product, product_quantity=product_quantity)
        cart_quantity =cart.__len__()
        print(cart_quantity)
        return JsonResponse(
            {
                "quantity": cart_quantity,
            }
        )


def cart_update(request):
    pass


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        cart.delete(product_id=product_id)
        cart_quantity =cart.__len__()
        cart_total = cart.get_total()
        return JsonResponse(
            {
                "quantity": cart_quantity,
                'total': cart_total,
            }
        )