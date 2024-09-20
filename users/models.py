from core import constants as const
from django.contrib.auth.models import AbstractUser
from django.db import models


class SarafanUser(AbstractUser):
    address = models.CharField(
        max_length=const.USER_ADDRESS_MAX_LENGTH,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=const.USER_EMAIL_MAXLENGHT,
        unique=True,
        error_messages={
            'unique': (
                const.USER_EMAIL_UNIQUE_ERROR_MESSAGE
            )
        },
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['first_name', 'email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.email}'
