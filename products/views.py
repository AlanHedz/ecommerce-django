from models import Product
from models import ShoppingCart
from models import InShoppingCart
from models import Order

from forms import CreateProductForm

from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy

class CreateClass(CreateView, LoginRequiredMixin):
	login_url = 'user:login'
	success_url = reverse_lazy('products:index')
	template_name = 'products/create.html'
	model = Product
	form_class = CreateProductForm

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())

class IndexClass(ListView, LoginRequiredMixin):
	login_url = 'user:login'
	template_name = 'products/index.html'

	def get_queryset(self):
		return Product.objects.all()

class ShowClass(DetailView):
	model = Product
	template_name = 'products/show.html'
	slug_url_kwarg = 'slug'

class EditClass(UpdateView, LoginRequiredMixin):
	login_url = 'user:login'
	template_name = 'products/edit.html'
	model = Product
	success_url = reverse_lazy('products:index')
	form_class = CreateProductForm

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(EditClass, self).form_valid(form)

class DeleteClass(DeleteView, LoginRequiredMixin):
	login_url = 'user:login'
	success_url = reverse_lazy('products:index')
	model = Product

def add_to_cart(request):
	if request.method == 'POST':
		shopping_cart_id = request.session.get('shopping_cart_id')
		shopping_cart = ShoppingCart.objects.findOrCreateBySessionId(shopping_cart_id)
		product = Product.objects.get(pk = request.POST['product_id'])
		response = InShoppingCart.objects.create(shopping_cart = shopping_cart, product = product)

		if request.is_ajax():
			products_count = InShoppingCart.objects.products_count(shopping_cart_id)
			return JsonResponse({'products_count': products_count})

		if response:
			return redirect('products:carrito')
		else:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return redirect('dashboard')

def carrito(request):
	shopping_cart_id = request.session.get('shopping_cart_id')
	shopping_cart = ShoppingCart.objects.findOrCreateBySessionId(shopping_cart_id)
	products = shopping_cart.products.all()
	total = shopping_cart.total()
	context = {'products': products, 'total': total, 'shopping_cart_id': shopping_cart_id}
	return render(request, 'shopping_cart/index.html', context)

def compras(request, custom_id):
	shop = get_object_or_404(ShoppingCart, customid=custom_id)
	order = Order.objects.get(shopping_cart = shop)
	return render(request, 'shopping_cart/completed.html', {'order': order, 'shop': shop})

@login_required(login_url = 'user:login')
def orders(request):
	orders = Order.objects.monthly()
	total_orders = Order.objects.total_month_count()
	total_month = Order.objects.total_month()
	return render(request, 'orders/index.html', {'orders': orders, 'total_orders': total_orders, 'total_month': total_month})


@csrf_exempt
@login_required(login_url = 'user:login')
def update_order(request, pk):
	order_update = Order.objects.get(pk=pk)
	name = request.POST.get('name')
	if name == 'guide_number':
		value = request.POST.get('value')
		order_update.guide_number = value
		order_update.save()
		return HttpResponse(value)
	elif name == 'status':
		value = request.POST.get('value')
		order_update.status = value
		order_update.save()
		return HttpResponse(value)