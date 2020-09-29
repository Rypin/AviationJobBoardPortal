from django import forms
from django.contrib.auth.models import User
from .models import CompanyProfile, applicationInfo
from django.contrib.auth.forms import UserCreationForm
from apply.models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class CompanyRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class CompanyUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Company Name', max_length=30)
    phoneNumber = forms.CharField(label='Phone Number', max_length=15)
    address = forms.CharField(label='Address', max_length=40)
    company_description = forms.CharField(label='Company Description', max_length=500)

    class Meta:
        model = CompanyProfile
        fields = ['image', 'banner','name', 'phoneNumber', 'address',
                  'company_description']

class CompanyProfileForm(forms.ModelForm):
    name = forms.CharField(label='Company Name', max_length=30)
    phoneNumber = forms.CharField(label='Phone Number', max_length=15)
    address = forms.CharField(label='Address', max_length=40)
    company_description = forms.CharField(label='Company Description', max_length=500)

    class Meta:
        model = CompanyProfile
        fields = ['name', 'phoneNumber', 'address',
                  'company_description']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = applicationInfo
        fields = "__all__"