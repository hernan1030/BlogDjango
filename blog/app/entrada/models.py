from django.db import models

# Desde el settings en base esta AUTH_USER_MODEL = "user.User" que hace referencia a tomo mi modelo de usuario personalizado lo traigo y lo utilizo en modelo entrada
from django.conf import settings

# para traer la hora actual en el save
from datetime import datetime, timedelta

# para que se creae un sllug convinado con titulos y segundos
from django.template.defaultfilters import slugify

# apps de terceros
from model_utils.models import TimeStampedModel


# from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


# manager creado desde el home
from app.entrada.manager import EntryManagers
# Create your models here.


class Category(TimeStampedModel):
    """  Categorias de una entrada  """

    short_name = models.CharField('Nombre corto', max_length=15, unique=True)
    name = models.CharField('Nombre', max_length=30)

    class Meta:
        verbose_name = 'Categoria'

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    """ etiquetas de un articulo """

    name = models.CharField('Nombre', max_length=30)

    class Meta:
        verbose_name = 'Etiqueta'

    def __str__(self):
        return self.name


class Entry(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    title = models.CharField('Titulo', max_length=200)
    resume = models.TextField('Resumen')
    content = RichTextField('contenido')
    public = models.BooleanField(default=False)
    image = models.ImageField('Imagen', upload_to='Entry',)
    portada = models.BooleanField(default=False)
    in_home = models.BooleanField(default=False)
    slug = models.SlugField(editable=False, max_length=300)

    objects = EntryManagers()

    class Meta:
        verbose_name = 'Entrada'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 1calculamos en total de la hora actual

        now = datetime.now()
        total_time = timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second
        )

        segundos = int(total_time.total_seconds())
        slug_unico = f'{self.title}{str(segundos)}'
        self.slug = slugify(slug_unico)
        print(slug_unico)
        super(Entry, self).save(*args, **kwargs)
