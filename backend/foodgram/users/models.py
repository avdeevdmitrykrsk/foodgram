# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# from content.models import Recipe


class FoodgramUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

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
