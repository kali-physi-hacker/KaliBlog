from django import forms 

from authentication.models import User 


class UserLoginForm(forms.Form):
    username = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255)

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ("first_name", "last_name", "email", "password")