from core import constants as const
from core.models import CategoryBaseModel, NameSlugBaseModel
from core.services.models_products_service import (get_uuid_image_name,
                                                   save_image_in_current_size)
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(CategoryBaseModel):

    class Meta(CategoryBaseModel.Meta):
        verbose_name = 'объект «Категория»'
        verbose_name_plural = 'объекты «Категорий»'
        default_related_name = 'category'


class Subcategory(CategoryBaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta(CategoryBaseModel.Meta):
        verbose_name = 'объект «Подкатегория»'
        verbose_name_plural = 'объекты «Подкатегорий»'


class Product(NameSlugBaseModel):
    price = models.PositiveIntegerField(verbose_name='Цена')
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        null=True,
        related_name='subcategory_products',
        verbose_name='Подкатегория'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        related_name='products',
        verbose_name='Категория'
    )

    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'объект «Продукт»'
        verbose_name_plural = 'объекты «Продуктов»'
        default_related_name = 'product'


class ProductImagesDesktop(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True,
                                verbose_name='Продукт',
                                related_name='product_images_desktop')
    image_detail = models.ImageField(
        upload_to='products/detail/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Фотография «Карточка»'
    )
    image_list = models.ImageField(
        upload_to='products/list/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Фотография «Каталог»'
    )
    image_thumbnail = models.ImageField(
        upload_to='products/thumbnails/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Фотография «Миниатюра»'
    )

    class Meta:
        default_related_name = 'product_images_desktop'
        verbose_name = '«Изображения продуктов»'
        verbose_name_plural = '«Изображения продуктов»'

    def save(self, *args, **kwargs):
        """Сохраняет изображение в трех размерах."""
        self.image_detail.name = get_uuid_image_name()
        super().save(*args, **kwargs)
        output_size_list = (const.PRODUCT_IMAGE_LIST_HEIGTH,
                            const.PRODUCT_IMAGE_LIST_WEIGHT)
        output_size_thumbnail = (const.PRODUCT_IMAGE_THUMBNAIL_HEIGTH,
                                 const.PRODUCT_IMAGE_THUMBNAIL_WEIGHT)
        image_list_path = save_image_in_current_size(
            self.image_detail, output_size_list, const.PATH_PART_IMAGE_LIST
        )
        image_thumbnail_path = save_image_in_current_size(
            self.image_detail, output_size_thumbnail,
            const.PATH_PART_IMAGE_THUMBNAIL
        )
        self.image_list = image_list_path
        self.image_thumbnail = image_thumbnail_path
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Десктопные фотографии товара {self.product}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name='shopping_cart',
                             verbose_name='Пользователь')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='shopping_cart',
                                verbose_name='Продукт')
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=const.DEFAULT_VALUE_OF_AMOUNT_OF_PRODUCTS
    )

    class Meta:
        default_related_name = 'shopping_cart'

    def __str__(self):
        return f'{self.user} - {self.product}'
