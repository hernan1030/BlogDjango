from django.db import models

# Desde el settings en base esta AUTH_USER_MODEL = "user.User" que hace referencia a tomo mi modelo de usuario personalizado lo traigo y lo utilizo en modelo entrada
from django.conf import settings

# aqui utulizamos apps de terceros ck editor
# pip install django-ckeditor
# apps de terceros
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField

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
    content = RichTextUploadingField('contenido')
    public = models.BooleanField(default=False)
    image = models.ImageField('Imagen', upload_to='Entry',)
    portada = models.BooleanField(default=False)
    in_home = models.BooleanField(default=False)
    slug = models.SlugField(editable=False, max_length=300)

    class Meta:
        verbose_name = 'Entrada'

    def __str__(self):
        return self.title
