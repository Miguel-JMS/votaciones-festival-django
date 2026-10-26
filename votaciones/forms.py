from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        correo = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return correo

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data["email"]
        if commit:
            usuario.save()
        return usuario
