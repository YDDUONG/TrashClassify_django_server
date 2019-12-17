from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    hashkey = forms.CharField()
    captcha = forms.CharField(label="验证码",min_length = 4, widget=forms.TextInput(attrs={'class': 'form-captcha','autocomplete':'off'}))
