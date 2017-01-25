from django import forms
from models import Product

class CreateProductForm(forms.ModelForm):
	title = forms.CharField(max_length=20)
	description = forms.CharField(max_length=150, widget=forms.Textarea)
	pricing = forms.CharField(widget=forms.NumberInput)

	def __init__(self, *args, **kwargs):
		super(CreateProductForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingreesa un titulo...'})
		self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa una descripcion del producto'})
		self.fields['pricing'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa el precio en centavos de dolar'})

	class Meta:
		model = Product
		fields = ('title', 'description', 'pricing')
