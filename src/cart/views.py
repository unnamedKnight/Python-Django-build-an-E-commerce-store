from django.shortcuts import render
from store.models import Product
from django.shortcuts import get_object_or_404


from .cart import Cart

# Create your views here.


def cart_summary(request):
    return render(request, 'cart/cart_summary.html')



def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, pk=product_id)
        cart.add(product=product, product_quantity=product_quantity)


def cart_update(request):
    pass



def cart_delete(request):
    pass