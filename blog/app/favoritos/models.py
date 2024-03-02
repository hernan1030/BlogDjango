from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings

#
from app.entrada.models import Entry
from .managers import ProfileEntada
# Create your models here.


class Favorites(TimeStampedModel):
    """ Modelo para favotios """

    # en ves de realizar la foreinkey desde el modelo se busca desde los setting
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_favorites', on_delete=models.CASCADE,)
    entry = models.ForeignKey(
        Entry, related_name='entry_favorites', on_delete=models.CASCADE)

    objects = ProfileEntada()

    class Meta:
        unique_together = ('user', 'entry')
        verbose_name = 'Entrada Favorita'

    def __str__(self):
        return self.entry.title
