from products.models import ShoppingCart
from products.models import Order

from django.conf import settings

from django.views.generic import RedirectView
from django.views.generic import TemplateView

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

import paypalrestsdk

class PaypalView(RedirectView):
	permanent = False

	def _generar_lista_items(self, shopping_cart):
		items = []
		products = shopping_cart.products.all()
		for product in products:
			title = product.paypal_item().get('name')
			sku = product.paypal_item().get('sku')
			price = product.paypal_item().get('price') / 100
			currency = product.paypal_item().get('currency')
			items.append({'name': str(title), 'sku': str(sku), 'price': str(price), 'currency': currency, 'quantity': 1})
		return items

	def _generar_peticion_pago_paypal(self, shopping_cart):
		peticion_pago = {
			'intent': 'sale',
			'payer': {'payment_method': 'paypal'},
			'redirect_urls':{
				'return_url': 'http://localhost:8000/paypal/create/',
				'cancel_url': 'http//localhost:8000/error'
			},
			'transactions':[{
				'item_list':{
					'items': self._generar_lista_items(shopping_cart)
				},
				'amount': {
					'total': shopping_cart.total(),
					'currency': 'USD'
				},
				'description': 'Tu compra en tiendus',
			}]}
		return peticion_pago

	def _generar_pago_paypal(self, shopping_cart):
		my_api = paypalrestsdk.Api({
			'mode': 'sandbox',
			'client_id': settings.PAYPAL_CLIENT_ID,
			'client_secret': settings.PAYPAL_CLIENT_SECRET
		})
		pago_paypal = paypalrestsdk.Payment(self._generar_peticion_pago_paypal(shopping_cart), api = my_api)

		if pago_paypal.create():
			for link in pago_paypal.links:
				if link.method == 'REDIRECT':
					url_pago = link.href
		else:
			raise Exception(pago_paypal.error)

		return url_pago, pago_paypal

	def get_redirect_url(self, *args, **kwargs):
		shopping_cart = get_object_or_404(ShoppingCart, pk = int(kwargs['shop_id']))
		url_pago, pago_paypal = self._generar_pago_paypal(shopping_cart)
		self.request.session['payment_id'] = pago_paypal.id
		return url_pago


def paypal_execute(request):
	payment_id = request.session['payment_id']
	payer_id = request.GET['PayerID']
	shopping_cart = request.session['shopping_cart_id']
	shop = ShoppingCart.objects.get(pk = shopping_cart)
	paypalrestsdk.configure({
		'mode': 'sandbox',
		'client_id': settings.PAYPAL_CLIENT_ID,
		'client_secret': settings.PAYPAL_CLIENT_SECRET
	})
	payment = paypalrestsdk.Payment.find(payment_id)
	if payment.execute({'payer_id': payer_id}):
		order = create_order(payment, shopping_cart)
		del request.session['shopping_cart_id']	
	return render(request, 'exito.html', {'order': order, 'shop': shop})


def create_order(payment, shopping_cart):
	email = payment.payer['payer_info']['email']
	recipient_name = payment.payer['payer_info']['first_name'] + " " + payment.payer['payer_info']['last_name']
	line1 = payment.payer['payer_info']['shipping_address']['line1']
	city = payment.payer['payer_info']['shipping_address']['city']
	postal_code = payment.payer['payer_info']['shipping_address']['postal_code']
	country_code = payment.payer['payer_info']['shipping_address']['country_code']
	state = payment.payer['payer_info']['shipping_address']['state']
	shop = ShoppingCart.objects.get(pk = shopping_cart)
	Order.objects.create(shopping_cart = shop,
		email = email, line1 = line1, city = city, postal_code = postal_code, 
		country_code = country_code, total = shop.total(), recipient_name = recipient_name, state = state)
	order = Order.objects.get(shopping_cart = shop)
	shop.approve()
	return order
		
			
		

		