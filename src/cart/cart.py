from decimal import Decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        if "session_key" not in request.session:
            # creating a session_key in the request.session aka self.session dictionary
            # if the user does not have a session_key
            cart = self.session["session_key"] = {}
        else:
            cart = self.session.get("session_key")

        self.cart = cart

    def add(self, product, product_quantity):
        """If product in cart then update the quantity if not then add it to the cart with price and quantity"""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = product_quantity
        else:
            self.cart[product_id] = {
                "price": str(product.price),
                "quantity": product_quantity,
            }

        self.session.modified = True

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product_id, product_quantity):
        product_id = str(product_id)
        product_quantity = product_quantity
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = product_quantity

        self.session.modified = True

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()
        # getting the products that matches the product id from all_product_ids
        products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()

        for product in products:
            # we are adding the product object to the cart
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total"] = item["price"] * item["quantity"]
            yield item

    def get_total(self):
        return sum(
            (
                Decimal(item["price"]) * Decimal(item["quantity"])
                for item in self.cart.values()
            )
        )
