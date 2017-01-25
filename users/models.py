from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager, models.Manager):
	def _create_user(self, username, email, password, is_staff, is_superuser, **kwargs):
		email = self.normalize_email(email)
		if not email:
			raise ValueError('El email debe ser obligatorio')
		user = self.model(username = username, email = email, is_active=True, is_staff = is_staff, is_superuser = is_superuser)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_user(self, username, email, password=None, **kwargs):
		return self._create_user(username, email, password, False, False, **kwargs)

	def create_superuser(self, username, email, password=None, **kwargs):
		return self._create_user(username, email, password, True, True, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=100, unique=True)
	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	avatar = models.ImageField(upload_to='users')

	objects = UserManager()

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_short_name(self):
		return self.username

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	bio = models.TextField()
	slug = models.CharField(max_length=100)

	def save(self, *args, **kwargs):
		self.slug = self.user.username.replace(' ', '-').lower()
		super(UserProfile, self).save(*args, **kwargs)

	def __str__(self):
		return self.user.username
    
