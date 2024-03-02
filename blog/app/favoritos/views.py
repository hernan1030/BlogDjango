# vitas
from django.views.generic import ListView, View, DeleteView

# Modelos
from app.entrada.models import Entry
from app.favoritos.models import Favorites


# redireccion
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# enviar mensaje de error
from django.contrib import messages  # Importar messages desde django.contrib


# para decorar y solo poder acceder si el usuario esta logueado
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class ProfileViews(ListView):
    template_name = 'perfil-favoritos/profile.html'
    context_object_name = 'entradas'

    def get_queryset(self):
        usuario = self.request.user
        resultado = Favorites.objects.entradas_users(usuario)

        return resultado


@method_decorator(login_required, name='dispatch')
class AgregarFavoritos(View):
    """
    de las entradas creadas , esta clase toma el usuario actual  y la entrada actual
    filtra si esta en modelo favorito con el if , si no esta lo coje y lo envia al perfil.
    - se crea con la vista generica View ya que no hace falta crear un formulario, lo que hace
    es toma la entrada ya existente y la envia por medio de la url de esa entrada


    """

    def post(self, request, *args, **kwargs):
        # recuperar el usuario y la pk del modelo
        usuario = self.request.user
        # me trae el title del modelo entry
        entrada = Entry.objects.get(id=self.kwargs['pk'])

        # verificar si la llave ya existe en los favoritos del usuario
        if Favorites.objects.filter(user=usuario, entry=entrada).exists():
            # Si la entrada ya existe lo redirecciono a su perfil
            messages.error(request, "La entrada ya está en tus favoritos.")
            return HttpResponseRedirect(reverse_lazy('profiles'))

        # si la entrada no existe en los favoritos del usuario, crearla
        try:
            Favorites.objects.create(user=usuario, entry=entrada)
            messages.success(
                request, "Entrada agregada a favoritos exitosamente.")
        except Entry.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('home'))

        return HttpResponseRedirect(reverse_lazy('profiles'))


# esta clase elimina del perfil la entrada existe , mas no del blog osea de las entradas
class DeleteFavoritos(DeleteView):
    template_name = 'perfil-favoritos/delete-entrada.html'
    model = Favorites
    success_url = reverse_lazy('profiles')
