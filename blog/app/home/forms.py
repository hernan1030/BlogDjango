# para utilizar modelo con meta ya hechos
from django import forms

# modelo del home
from .models import Suscribers, Contact


from django.core.exceptions import ValidationError


# se envia el formulario con widges personalizado
class HomePageForm(forms.ModelForm):

    class Meta:
        model = Suscribers
        fields = ['email']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu email'})
        }
        labels = {
            'email': 'Suscribete'  # Aquí se especifica el label para el campo 'email'
        }


class ContacForms(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'messagge']
