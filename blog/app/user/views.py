

# vistas genericas
from django.views.generic import FormView


# formularios desde el forms.py
from .forms import RegisterForms, LoginForm, CodeRegistroForm, UpdatePasswordForm

# redireccion de paginas
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Para envio de email de prueba
from django.core.mail import send_mail

# Para autenticar el usuario
from django.contrib.auth import authenticate, login, logout


# modelo usuario
from .models import User


# funciones extras de funtions.py
from .funtions import code_numrandom
from blog.settings.base import get_secret


# para decorar y solo poder acceder si el usuario esta logueado
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Crea la vistas aqui:


# Vista para el registro de usuario
class RegisterViews(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForms
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        codigo = code_numrandom()

        usuario = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1']
        )

        # Guardar campos adicionales del usuario
        usuario.ocupation = form.cleaned_data['ocupation'].lower(),
        usuario.genero = form.cleaned_data['genero'].lower()
        usuario.full_name = form.cleaned_data['full_name'],
        usuario.date_birth = form.cleaned_data['date_birth']
        usuario.verificationcode = codigo
        usuario.save()

       # Variables para envio de email
        asunto = 'Confirmacion de email'
        mensaje = f'Codigo de verificacion de registro: {codigo}'
        email_remitente = get_secret('EMAIL')

        # Enviar correo electrónico de confirmación
        send_mail(
            asunto, mensaje, email_remitente, [form.cleaned_data['email'],]
        )

        return HttpResponseRedirect(reverse_lazy('confi_email', kwargs={'pk': usuario.pk}))


# Vista para el login de usuario
class LoginViews(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        usuario = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        login(self.request, usuario)

        return super().form_valid(form)


# Salir de la seccion de logion
class LogoutViews(FormView):

    def get(self, request, *args, **kwars):

        logout(request)

        return HttpResponseRedirect(reverse_lazy('login'))


# Confirmacion de email
class ConfirmacionEmailViews(FormView):
    template_name = "users/confi_email.html"
    form_class = CodeRegistroForm
    success_url = reverse_lazy('login')

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        # Obtener pk de los argumentos de la URL
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        # Marcar al usuario como activo
        User.objects.filter(
            id=self.kwargs['pk']

        ).update(
            is_active=True
        )

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UpdatePasswordViews(FormView):
    template_name = 'users/update-password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )
        if user:
            nuevo_password = form.cleaned_data['password2']
            usuario.set_password(nuevo_password)
            usuario.save()

        logout(self.request)

        return super(UpdatePasswordViews, self).form_valid(form)
