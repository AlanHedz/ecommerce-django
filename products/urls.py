from django.conf.urls import url
from views import CreateClass
from views import IndexClass
from views import ShowClass
from views import EditClass
from views import DeleteClass
from views import add_to_cart
from views import carrito
from paypal_configure import PaypalView
from paypal_configure import paypal_execute
from views import compras
from views import orders
from views import update_order

app_name = 'products'

urlpatterns = [
	url(r'^products/create/$', CreateClass.as_view(), name = 'create'),
	url(r'^products/$', IndexClass.as_view(), name = 'index'),
	url(r'^products/(?P<slug>[-\w]+)/$', ShowClass.as_view(), name = 'show'),
	url(r'^products/edit/(?P<pk>\d+)/$', EditClass.as_view(), name = 'edit'),
	url(r'^products/delete/(?P<pk>\d+)/$', DeleteClass.as_view(), name = 'delete'), 
	url(r'^add/$', add_to_cart, name = 'add'),
	url(r'^paypal-view/(?P<shop_id>\d+)/$', PaypalView.as_view(), name = 'paypal-view'),
	url(r'^paypal/create/$', paypal_execute, name = 'paypal-execute'),
	url(r'^carrito/$', carrito, name = 'carrito'),
	url(r'^compras/(?P<custom_id>[-\w]+)/$', compras, name = 'order'),
	url(r'^orders/$', orders, name='orders'),
	url(r'^orders/(?P<pk>\d+)/$', update_order, name = 'update_order'),
]