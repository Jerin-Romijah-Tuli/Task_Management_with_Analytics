# users/forms.py

from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'address', 'mobile_number', 'date_of_birth', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
