# para realizar formularios personalizados
from django import forms

# Importaciones para autenticacion de usuario
from django.contrib.auth import authenticate

# validaciones para la contraseña
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator


from django.core.exceptions import ValidationError

# modelo user
from .models import User


class validator_password(forms.Form):

    pass


class RegisterForms(forms.ModelForm):

    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña1'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña2'}))

    class Meta:
        model = User
        fields = ['email', 'full_name', 'ocupation', 'genero', 'date_birth']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Completo'}),
            'ocupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ocupacion'}),
            'genero': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'date_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de nacimiento'})
        }

        labels = {
            'email': '', 'full_name': '', 'ocupation': '', 'genero': '', 'date_birth': ''
        }

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2:
            try:
                validator_password(password1)
                validator_password(password2)
                CommonPasswordValidator().validate(password1)
                NumericPasswordValidator().validate(password1)
            except forms.ValidationError as e:
                msg = f'La contraseña no es valida , {",".join(e)}'
                self.add_error('password1', msg)
            if password1 != password2:
                self.add_error(
                    'password2', 'Las contraseñas no coinciden ')

        return password1


class LoginForm(forms.Form):

    email = forms.CharField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    def clean(self):

        ususario = authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        if not ususario:
            raise forms.ValidationError(
                "El correo o la contraseña son incorrectas")

        return super().clean()


# Formulario para el código de confirmación del registro del usuario
class CodeRegistroForm(forms.Form):

    # aqui creo lo que mostrare en formulario
    codigoregistro = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ingresa codigo'}))

    """__init__(): Se utiliza para inicializar el formulario. 
    Aquí se pasa el pk como argumento y se guarda en self.id_user"""

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(CodeRegistroForm, self).__init__(*args, **kwargs)

    def clean_codigoregistro(self):
        codigo = self.cleaned_data['codigoregistro']

        if len(codigo) != 6:
            raise ValidationError(
                f'El codigo es incorrecto, solo tiene {len(codigo)} y debe ser 6 ')

        if not User.objects.codigo_validacio(self.id_user, codigo):
            raise forms.ValidationError('El codigo es incorrecto...')


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contraseña nueva'}))
