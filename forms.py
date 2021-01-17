from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SeamUser
'''
class UserForm(UserCreationForm):
    class Meta:
        model = SeamUser
        fields = ['username', 'password']

#회원정보 바꾸는 Form
class UserChangeForm(UserChangeForm):
    class Meta:
        model = SeamUser
        fields = ('username','password')

class LoginForm(forms.ModelForm):
    class Meta:
        model = SeamUser
        fields = ['username', 'password']
'''