# Thirdparty imports
from django.contrib.auth import get_user_model
from django.db import models

# Projects imports
from content.constants import LONG_STR_CUT_VALUE

User = get_user_model()


class FavoriteSgoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        'content.Recipe',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'recipe')
        abstract = True
        ordering = ('user', 'recipe')

    def __str__(self):
        from content.models import Recipe
        return f'{self.user} has a {self.recipe[:LONG_STR_CUT_VALUE]}.'
