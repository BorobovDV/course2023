from django import forms

class Authentication(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={"type": "text", "placeholder": "Логин"}))
    passwd = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "placeholder": "Пароль"}))


class Registration(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": "text", "placeholder": "Почта"}))
    login = forms.CharField(widget=forms.TextInput(attrs={"type": "text", "placeholder": "Логин"}))
    passwd = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "placeholder": "Пароль"}))
    passwd_check = forms.CharField(widget=forms.TextInput(attrs={"type": "password", "placeholder": "Повторите пароль"}))
