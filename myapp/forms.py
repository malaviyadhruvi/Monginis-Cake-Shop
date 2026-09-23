from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['user_name', 'email', 'password', 'gender', 'mob_num', 'city']
        widgets = {
            'password': forms.PasswordInput(),
        }
