from models import User
from models import UserProfile
from django import forms

class LoginUserForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=20, widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'form-control'})
		self.fields['password'].widget.attrs.update({'class': 'form-control'})

class RegisterUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=20, widget=forms.PasswordInput)
	email = forms.CharField()

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email).count():
			raise forms.ValidationError('El email ya existe, intenta con otro.')
		return email

	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'form-control'})
		self.fields['password'].widget.attrs.update({'class': 'form-control'})
		self.fields['email'].widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class EditUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, label='Usuario')
	email = forms.CharField(max_length=20, label='Email')
	first_name = forms.CharField(max_length=20, label='Nombre')
	last_name = forms.CharField(max_length=20, label='Apellido')
	avatar = forms.CharField(max_length=20, widget=forms.ClearableFileInput)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email).exclude(pk = self.instance.id).count():
			raise forms.ValidationError('El email ya existe, intenta con otro.')
		return email

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'avatar')

class EditProfileForm(forms.ModelForm):
	bio = forms.CharField(max_length=150, widget=forms.Textarea)

	class Meta:
		model = UserProfile
		fields = ('bio',)
    
    

    