from __future__ import unicode_literals
from users.models import User
from django.db.models import Sum
from django.db.models import F, FloatField
from django.db import models
import hashlib
from datetime import date, datetime, timedelta

class Product(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=200)
	pricing = models.DecimalField(max_digits = 9, decimal_places = 2)
	slug = models.CharField(max_length=50)

	def save(self, *args, **kwargs):
		self.slug = self.title.replace(' ', '-').lower()
		super(Product, self).save(*args, **kwargs)

	def pricing_in_dolar(self):
		return self.pricing / 100

	def paypal_item(self):
		return {'name': self.title, 'sku': self.id, 'price': self.pricing, 'currency': 'USD'}

	def __str__(self):
		return self.title

class ShoppingCartQuerySet(models.QuerySet):
	def findBySession(self, shopping_cart_id):
		return self.get(pk = shopping_cart_id)

class ShoppingCartManager(models.Manager):
	def get_queryset(self):
		return ShoppingCartQuerySet(self.model, using=self._db)

	def createWithoutSession(self):
		shopping_cart = self.model(status = 'incompleted')
		shopping_cart.save(using = self._db)
		return shopping_cart

	def findOrCreateBySessionId(self, shopping_cart_id):
		if shopping_cart_id:
			return self.get_queryset().findBySession(shopping_cart_id)
		else:
			return self.createWithoutSession()
	

class ShoppingCart(models.Model):
	status = models.CharField(max_length=100)
	products = models.ManyToManyField(Product, through='InShoppingCart')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	customid = models.CharField(max_length=150 ,unique=True, null=True)
	objects = ShoppingCartManager.from_queryset(ShoppingCartQuerySet)()

	def products_size(self):
		return self.products.count()

	def total(self):
		return self.products.all().aggregate(pricing = Sum('pricing', output_field = FloatField())).get('pricing') / 100

	def generate_custom_id(self):
		return hashlib.sha224(str(self.id) + str(self.updated_at) ).hexdigest()

	def update_custom_id(self):
		self.status = 'approved'
		self.customid = self.generate_custom_id()
		self.save()

	def approve(self):
		self.update_custom_id()

class InShoppingCartQuerySet(models.QuerySet):
	def products_count(self, shopping_cart_id):
		return self.filter(shopping_cart__pk = shopping_cart_id).count()

class InShoppingCart(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now_add=True)
	objects = InShoppingCartQuerySet().as_manager()

class OrderQuerySet(models.QuerySet):

	def monthly(self):
		last_month = datetime.today() - timedelta(days=30)
		return self.filter(created_at__gte=last_month).order_by('id')

	def total_month(self):
		orders_lastmonth = self.monthly()
		return orders_lastmonth.aggregate(total = Sum('total', output_field = FloatField())).get('total')

	def total_month_count(self):
		orders_lastmonth = self.monthly()
		return orders_lastmonth.count()

class Order(models.Model):
	shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
	recipient_name = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	line1 = models.TextField(max_length=200)
	guide_number = models.CharField(max_length=50, null=True)
	postal_code = models.CharField(max_length=50)
	country_code = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	status = models.CharField(max_length=50, default="creado")
	total = models.DecimalField(max_digits=9, decimal_places=2)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now_add=True)
	objects = OrderQuerySet().as_manager()