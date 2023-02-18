from django import forms

class UserRegisterForm(forms.Form):
    """from for user registeration"""
    username = forms.CharField(max_length=64, required=True,
                               widget=forms.TextInput(attrs={'calss':'form-control'}))
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'calss':'form-control', 'placeholder':'example@mail.com'}))
    password = forms.CharField(max_length=32, required=True,
                               widget=forms.PasswordInput(attrs={'calss':'form-control', 'placeholder':'more than 8 character'}))