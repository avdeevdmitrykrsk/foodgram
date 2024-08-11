# Thirdparty imports
from django.contrib.auth import get_user_model
from django.db import models

# Projects imports
from content.models import Recipe

User = get_user_model()


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribe_list_by_user'
    )
    subscribe_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list_by_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_list_by_recipe'
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_by_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_list_by_recipe'
    )
