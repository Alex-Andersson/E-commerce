from typing import Any

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput, TextInput

# Register Form

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].required = True
        
    # Email Validation
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email is Invalid")
        
        if len(email) > 50:
            raise forms.ValidationError("Email is too long")

        return email
    
# Login Form

class LoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
# Update User Form

class UpdateUserForm(forms.ModelForm):
    
    password = None 
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].required = True
    
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']