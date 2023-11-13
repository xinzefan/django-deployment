from django import forms
from django.contrib.auth.models import User
from firstapp.models import UserProfileInfo
from django.core import validators

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User 
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

# class NewUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'