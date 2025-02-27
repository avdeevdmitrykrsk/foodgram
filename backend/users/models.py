# Thirdparty imports
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Exists, OuterRef
from django.contrib.auth.models import UserManager

# Projects imports
from content.constants import LONG_STR_CUT_VALUE
from users.constants import (USER_EMAIL_LENGTH, USER_FIRSTNAME_LENGTH,
                             USER_LASTNAME_LENGTH, USER_USERNAME_LENGTH)


class FoodgramuserManager(UserManager):

    def get_annotated_queryset(self, user):
        queryset = super().get_queryset()
        if user.is_authenticated:
            return queryset.annotate(
                is_subscribed=Exists(
                    Subscribe.objects.filter(
                        user=user, subscribe_to=OuterRef('pk')
                    )
                ),
            ).order_by('username',)
        return queryset


class FoodgramUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        unique=True,
        max_length=USER_USERNAME_LENGTH,
        verbose_name='username',
        validators=[UnicodeUsernameValidator()],
    )
    first_name = models.CharField(
        max_length=USER_FIRSTNAME_LENGTH,
        verbose_name='first_name'
    )
    last_name = models.CharField(
        max_length=USER_LASTNAME_LENGTH,
        verbose_name='last_name'
    )
    email = models.EmailField(
        unique=True,
        max_length=USER_EMAIL_LENGTH,
        verbose_name='email'
    )
    avatar = models.ImageField(
        upload_to='users/images/',
        null=True,
        default=None
    )

    objects = FoodgramuserManager()

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:LONG_STR_CUT_VALUE]


class Subscribe(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='subscribe_list_by_user'
    )
    subscribe_to = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='subscribe_list_by_subscribe_to'
    )

    class Meta:
        ordering = ('user', 'subscribe_to')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'subscribe_to'),
                name='unique_user_subscribe_to'
            )
        ]
