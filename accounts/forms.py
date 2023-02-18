from django import forms

class UserRegisterForm(forms.Form):
    """from for user registeration"""
    username = forms.CharField(max_length=64, required=True)
    email    = forms.EmailField(required=False)
    password = forms.CharField(max_length=32, required=True)