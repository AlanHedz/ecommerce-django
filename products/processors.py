from .models import ShoppingCart

def shopping_cart_procesor(request):
	shopping_cart_id = request.session.get('shopping_cart_id')
	shopping_cart = ShoppingCart.objects.findOrCreateBySessionId(shopping_cart_id)
	request.session['shopping_cart_id'] = shopping_cart.id
	context = {'products_count': shopping_cart.products_size}
	return context

		