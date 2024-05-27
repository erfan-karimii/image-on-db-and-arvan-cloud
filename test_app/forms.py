from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    main_image = forms.ImageField()
    class Meta:
        model = Product
        fields = '__all__'
    
    