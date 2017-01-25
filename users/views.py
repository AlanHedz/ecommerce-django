from models import User
from models import UserProfile

from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView

from forms import LoginUserForm
from forms import RegisterUserForm

from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy

class LoginClass(View):
	template = 'users/login.html'
	form = LoginUserForm()
	message = None

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('dashboard')
		return render(request, self.template, self.get_context())

	def post(self, request, *args, **kwargs):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login_django(request, user)
				return redirect('dashboard')
		return render(request, self.template, self.get_context())

	def get_context(self):
		return {'form': self.form}

class RegisterClass(View):
	template = 'users/signup.html'
	form = RegisterUserForm()

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('dashboard')
		return render(request, self.template, self.get_context())

	def post(self, request, *args, **kwargs):
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		user_create = User.objects.create_user(username = username, email = email, password = password)
		UserProfile.objects.create(user = user_create)
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login_django(request, user)
				return redirect('dashboard')
		return render(request, self.template, self.get_context())

	def get_context(self):
		return {'form': self.form}

def logout(request):
	logout_django(request)
	return redirect('user:login')

def method_login(request, username, password):
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login_django(request, user)
			return redirect('dashboard')