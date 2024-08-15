# Thirdparty imports
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Projects imports
from content.constants import (INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
                               INGREDIENT_NAME_MAX_LENGTH, LONG_STR_CUT_VALUE,
                               MAX_COOKING_TIME_VALUE, MAX_INGREDIENTS_AMOUNT,
                               MIN_COOKING_TIME_VALUE, MIN_INGREDIENTS_AMOUNT,
                               RECIPE_NAME_MAX_LENGTH, TAG_NAME_MAX_LENGTH,
                               TAG_SLUG_MAX_LENGTH)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=TAG_NAME_MAX_LENGTH,
        verbose_name='Название',
        help_text=(
            f'Максимально допустимое число знаков - {TAG_NAME_MAX_LENGTH}.'
        ),
        unique=True,
        db_index=True
    )
    slug = models.SlugField(
        max_length=TAG_SLUG_MAX_LENGTH,
        verbose_name='Слаг',
        help_text=(
            f'Максимально допустимое число знаков - {TAG_SLUG_MAX_LENGTH}.'
        ),
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name[:LONG_STR_CUT_VALUE]


class Ingredient(models.Model):
    name = models.CharField(
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        verbose_name='Название',
        help_text=(
            'Максимально допустимое число знаков - ',
            f'{INGREDIENT_NAME_MAX_LENGTH}.'
        )
    )
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name='Единица измерения',
        help_text=(
            'Максимально допустимое число знаков - ',
            f'{INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH}.'
        )
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name[:LONG_STR_CUT_VALUE]


class Recipe(models.Model):
    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH,
        db_index=True,
        verbose_name='Название',
        help_text=(
            f'Максимально допустимое число знаков - {RECIPE_NAME_MAX_LENGTH}.'
        )
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления (в минутах).',
        validators=[
            MinValueValidator(MIN_COOKING_TIME_VALUE),
            MaxValueValidator(MAX_COOKING_TIME_VALUE)
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        related_name='recipes_by_tag',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipes_by_ingredient',
        through='IngredientRecipe'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes_by_author'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    class Meta:
        ordering = ('name', 'author')
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:LONG_STR_CUT_VALUE]


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Колличество',
        help_text='Колличество ингредиентов',
        validators=[
            MinValueValidator(MIN_INGREDIENTS_AMOUNT),
            MaxValueValidator(MAX_INGREDIENTS_AMOUNT)
        ]
    )

    class Meta:
        default_related_name = 'get_ingredient_recipe'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} include {self.ingredient} with {self.amount}'


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
        abstract = True
        ordering = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} has a {self.recipe[:LONG_STR_CUT_VALUE]}.'


class Favorite(FavoriteSgoppingCart):

    class Meta(FavoriteSgoppingCart.Meta):
        default_related_name = 'favorite_list'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]


class ShoppingCart(FavoriteSgoppingCart):

    class Meta(FavoriteSgoppingCart.Meta):
        default_related_name = 'shopping_cart_list'
        verbose_name = 'Добавлен в корзину'
        verbose_name_plural = 'Добавлены в корзину'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_user_recipe'
            )
        ]
