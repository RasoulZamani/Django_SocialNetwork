from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.Form):
    """from for user registeration"""
    username = forms.CharField(max_length=64, required=True,
        widget=forms.TextInput(attrs={'calss':'form-control'}))
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'calss':'form-control', 'placeholder':'example@mail.com'}))
    password = forms.CharField(max_length=32, min_length=8, required=True,
        widget=forms.PasswordInput(attrs={'calss':'form-control', 'placeholder':'more than 8 character'}))
    
    def clean_email(self):
        """checkimg uniqeness of email"""
        input_email = self.cleaned_data['email']
        user_with_email = User.objects.filter(email=input_email).exists()
        if user_with_email:
            raise ValidationError("This email is already exist!")
        return input_email
    
    def clean_username(self):
        """checkimg uniqeness of username"""
        input_username = self.cleaned_data['username']
        user_with_username = User.objects.filter(username=input_username).exists()
        if user_with_username:
            raise ValidationError("This username is already exist!")
        return input_username