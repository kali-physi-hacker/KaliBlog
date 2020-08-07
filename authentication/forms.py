from django import forms 

from authentication.models import User 


class UserLoginForm(forms.Form):
    username = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255)


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ("first_name", "last_name", "email")

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return data['password2']

    def clean_email(self):
        return self.cleaned_data.get("email").lower()
