from django import forms


class Login(forms.Form):
    user_id = forms.CharField(label="User Id", max_length=200)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
