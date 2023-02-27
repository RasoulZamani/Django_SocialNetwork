from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegisterForm(forms.Form):
    """from for user registeration"""
    username = forms.CharField(max_length=64, required=True,
        widget=forms.TextInput(attrs={'calss':'form-control'}))
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'calss':'form-control', 'placeholder':'example@mail.com'}))
    password = forms.CharField(max_length=32, min_length=8, required=True,
        widget=forms.PasswordInput(attrs={'calss':'form-control', 'placeholder':'more than 8 character'}))
    confired_pass = forms.CharField(label='Confime Password', max_length=32, min_length=8, required=True,
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
    
    def clean(self):
        """overwritin clean for validating two fields (pass and conformed pass)"""
        cd = super().clean()
        password = cd.get('password')
        confired_pass=cd.get('confired_pass')
        
        if password and confired_pass and (password != confired_pass):
            raise ValidationError('two password must match') 
        

class UserLoginForm(forms.Form):
    """from for user login"""
    username = forms.CharField( required=True,
        widget=forms.TextInput(attrs={'calss':'form-control', 'placeholder':'username or email'}))
    password = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={'calss':'form-control'}))
    

class EditProfileForm(forms.ModelForm):
    """Form for editting profile"""
    
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ('age', 'bio')