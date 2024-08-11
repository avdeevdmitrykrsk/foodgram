# Thirdparty imports
from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodgramUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='username'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email'
    )
    avatar = models.ImageField(
        upload_to='users/images/',
        null=True,
        default=None
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
