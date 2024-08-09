from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        db_index=True
    )
    slug = models.SlugField(
        max_length=256,
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=16,
        verbose_name='Единица измерения',
        help_text='Единица измерения'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Максимально допустимое число знаков - 256.'
    )
    text = models.TextField(
        max_length=1200,
        verbose_name='Текст',
        help_text='Максимально допустимое число знаков - 1200.'
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления (в минутах).',
        validators=[
            MinValueValidator(settings.MIN_COOKING_TIME_VALUE)
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
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='amount_by_ingredient',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    amount = models.SmallIntegerField(
        verbose_name='Колличество',
        help_text='Колличество ингредиентов',
        default=0,
        validators=[
            MinValueValidator(settings.MIN_INGREDIENTS_AMOUNT)
        ]
    )

    class Meta:
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe}'
