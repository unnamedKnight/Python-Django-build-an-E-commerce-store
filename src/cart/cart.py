class Cart:
    def __init__(self, request):
        self.session = request.session
        if 'session_key' not in request.session:
            # creating a session_key in the request.session aka self.session dictionary
            # if the user does not have a session_key
            cart = self.session['session_key']={}
        else:
            cart = self.session.get('session_key')

        self.cart = cart
