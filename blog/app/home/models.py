
from django.db import models


# INSTALLA  django model utilis
# pip install django-model-utils
# apps terceros
# con el timeStampedModel ya nos tra fecha de creacion y de actulizacion y los models
from model_utils.models import TimeStampedModel

# Create your models here.

"""
con este modelo se envian varios contextos al home
title es el titulo de la pagina enviada al home
description : es la descrpcion del contenido debajo del titulo
about_title: es el titulo de nostros
about_text: donde escribimo el mas sobre notros
contac_email: correo donde nos contactan desde home se muestra
phone: numero de telefono que se muestra desde el home
"""


class Home(TimeStampedModel):
    """ Model para datos de la pantalla home  """
    title = models.CharField('Nombre', max_length=30)
    description = models.TextField()
    about_title = models.CharField('Titulo Nosotros', max_length=50)
    about_text = models.TextField()
    contact_email = models.EmailField(
        'email de contacto', blank=True, null=True)
    phone = models.CharField('Telefono contacto', max_length=20)

    class Meta:
        verbose_name = 'Pagina Principal'

    def __str__(self):
        return self.title


# este modelo es un campo de solo email para la suscrpcion de la pagina desde el home
class Suscribers(TimeStampedModel):
    """ Suscripciones """

    email = models.EmailField()

    class Meta:
        verbose_name = 'Suscriptor'

    def __str__(self):
        return self.email


# este modelo se utiliza para el formulario para que te contacte ubicado en home
class Contact(TimeStampedModel):
    """ Formulario de Contacto """

    full_name = models.CharField('Nombres', max_length=60)
    email = models.EmailField()
    messagge = models.TextField()

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return self.full_name
