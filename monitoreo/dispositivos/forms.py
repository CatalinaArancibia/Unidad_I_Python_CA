from django import forms
from django.contrib.auth.models import User
from .models import Organization
import re

class OrganizationForm(forms.ModelForm):
    username = forms.CharField(label="Usuario")
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Organization
        fields = ['organization_name', 'organization_description']
        labels = {
            'organization_name': 'Nombre Empresa',
            'organization_description': 'Descripción Empresa',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo ya está registrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El usuario ya está registrado.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not re.search(r'[\W_]', password):
            raise forms.ValidationError(
                "La contraseña no cumple con los requisitos de seguridad."
            )
        return password

class OrganizationLoginForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nueva Contraseña", min_length=8)