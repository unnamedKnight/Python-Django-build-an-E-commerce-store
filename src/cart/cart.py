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
        print('Cart.add is running')
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = product_quantity
        else:
            self.cart[product_id] = {
                "price": str(product.price),
                "quantity": product_quantity,
            }

        self.session.modified = True


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
