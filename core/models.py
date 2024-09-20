from core import constants as const
from django.db import models


class NameSlugBaseModel(models.Model):
    name = models.CharField(
        max_length=const.NAME_BASE_MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=const.SLUG_BASE_MAX_LENGTH,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class CategoryBaseModel(NameSlugBaseModel):
    image = models.ImageField(
        upload_to='categories/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Фотография'
    )

    class Meta(NameSlugBaseModel.Meta):
        abstract = True
