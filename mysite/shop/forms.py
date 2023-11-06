from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Product, Category, User_profile, User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'product_name', 'product_category', 'product_description', 'product_discount', 'product_price',
            'product_image'
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        ordering = ['category_name']
        fields = (
            'category_name',
        )




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_profile
        fields = ['name', 'last_name', 'birthday', 'photo', 'gender', 'city', 'email', 'phone_number']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
