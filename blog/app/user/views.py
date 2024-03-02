

# vistas genericas
from django.views.generic import FormView


# formularios desde el forms.py
from .forms import RegisterForms, LoginForm, CodeRegistroForm, UpdatePasswordForm

# redireccion de paginas
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

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
        # Generar código de verificación
        codigo = code_numrandom()

        # se pasa estos campos desde el managers.py campos originales
        usuario = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1']
        )

        # Guardar campos adicionales del usuario
        usuario.ocupation = form.cleaned_data['ocupation'].lower()
        usuario.genero = form.cleaned_data['genero'].lower()
        usuario.full_name = form.cleaned_data['full_name'].lower()
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

        # Luego del registro,redirege al usuario al confi_email , le pasamo el usuario.pk el id del usuario registrado
        return HttpResponseRedirect(reverse_lazy('confi_email', kwargs={'pk': usuario.pk}))


# Vista para el login de usuario
class LoginViews(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('profiles')

    def form_valid(self, form):
        """
         con este form_valid despues de rellanar los datos en el tamplate verfica con el
         autenticate si existe en la base de datos con el clean_data recoje lo que manda el 
         usuario y si existe lo redirige al perfil        
        """
        usuario = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        login(self.request, usuario)

        return super().form_valid(form)


# Salir de la seccion de logion
class LogoutViews(FormView):

    """lo saca de la seccion que este actualmete conctada"""

    def get(self, request, *args, **kwars):

        logout(request)

        return HttpResponseRedirect(reverse_lazy('login'))


# Confirmacion de email
class ConfirmacionEmailViews(FormView):
    template_name = "users/confi_email.html"
    form_class = CodeRegistroForm
    success_url = reverse_lazy('login')

    def get_form_kwargs(self):
        """
        este metodo lo que hace es recoger el id del usuario registrado
        en el registerView y lo guarda en la variable kwars y se puede uyilizar luego en 
        toda la clase actual
        """
        kwargs = super().get_form_kwargs()
        # Obtener pk de los argumentos de la URL
        kwargs['pk'] = self.kwargs['pk']

        return kwargs

    # envia el id se usuario al html y cuando se envia el formulario entra como un campo oculto
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['user_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        # recoge el id del usuario registrado
        user_id = self.kwargs['pk']

        # Marcar al usuario como activo
        User.objects.filter(id=user_id).update(is_active=True)

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Guardar el ID del usuario en la sesión
        self.request.session['user_id'] = self.kwargs['pk']
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UpdatePasswordViews(FormView):
    """Cambiar contraseña"""
    template_name = 'users/update-password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # trae el usuario actual
        usuario = self.request.user

        """con autenticate verificamos si el campo email coniciden con usuario.email
           registrado ya anteriormente y le pasamos la contraseña, si el usuario es Tre
           creamos una nuevo_passwor con set_password lo actualizamos y luego guardamos
        """
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


"""

class ConfirmacionEmailViews(FormView):
    template_name = "users/confi_email.html"
    form_class = CodeRegistroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Obtener el ID del usuario de la sesión
        user_id = self.request.session.get('user_id')
        
        # Marcar al usuario como activo
        User.objects.filter(id=user_id).update(is_active=True)

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Guardar el ID del usuario en la sesión
        self.request.session['user_id'] = self.kwargs['pk']
        return super().dispatch(request, *args, **kwargs)

"""


"""
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

"""
