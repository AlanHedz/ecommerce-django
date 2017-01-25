from products.models import ShoppingCart
from products.models import Product
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy

def home(request):
	shopping_cart_id = request.session.get('shopping_cart_id')
	shopping_cart = ShoppingCart.objects.findOrCreateBySessionId(shopping_cart_id)
	request.session['shopping_cart_id'] = shopping_cart.id
	products = Product.objects.all().order_by('id')
	pagination = Paginator(products, 5) 
	return render(request, 'home.html', {'products': products, 'pagination': pagination})

@login_required(login_url = 'user:login')
def dashboard(request):
	return render(request, 'dashboard.html', {})