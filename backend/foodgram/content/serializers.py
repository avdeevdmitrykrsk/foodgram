from django.conf import settings
from django.db.models import F
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError

from content.models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
)
from users.serializers import UserSerializer
from users.utils import Base64ToAvatar, check_list
from users_feature.models import Favorite, ShoppingCart

EXPECTED_RECIPE_FIELD = ('ingredients', 'tags')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientRecipe
        fields = ('amount',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class GetRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(
        method_name='make_data',
        validators=[UniqueValidator(queryset=Tag.objects.all(),)]
    )
    tags = TagSerializer(
        read_only=True, many=True,
        validators=[UniqueValidator(queryset=Tag.objects.all(),)]
    )
    author = UserSerializer(read_only=True)
    image = Base64ToAvatar()
    is_favorited = serializers.SerializerMethodField(
        method_name='check_favorite'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='check_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def check_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            shopping_cart_list = ShoppingCart.objects.filter(
                user=user
            )
            return check_list(obj, shopping_cart_list, 'recipe')
        return False

    def check_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            favorite_list = Favorite.objects.filter(
                user=user
            )
            return check_list(obj, favorite_list, 'recipe')
        return False

    def make_data(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('amount_by_ingredient__amount')
        )


class RecipeSerializer(GetRecipeSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )
        extra_kwargs = {
            'ingredients': {'required': True},
            'tags': {'required': True},
            'image': {'required': True},
            'name': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True}
        }

    def validate(self, validated_data):
        for field in EXPECTED_RECIPE_FIELD:
            error_message = f'Неправильное значение поля {field}'
            if not self.initial_data.get(field):
                raise ValidationError(error_message)
            for ingredient in self.initial_data.get(field):
                print(ingredient.get('id'))
                if ingredient['id'] < settings.MIN_INGREDIENTS_AMOUNT:
                    raise ValidationError(
                        f'{field} не может быть меньше 1.'
                    )
                if (
                    not Ingredient.objects.filter(
                        id=ingredient['id']
                    ).exists()
                ):
                    raise ValidationError(error_message)
        return validated_data

    def create(self, validated_data):
        tags_values = self.initial_data.pop('tags')
        ingredients_values = self.initial_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data
        )
        for ingredient in ingredients_values:
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=Ingredient.objects.get(
                    id=ingredient['id']
                )
            )
        for _ in tags_values:
            recipe.tags.set(tags_values)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.image = validated_data['image']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']

        tags_values = self.initial_data.pop('tags')
        for _ in tags_values:
            instance.tags.set(tags_values)

        ingredients_values = self.initial_data.pop('ingredients')
        instance.amount_by_ingredient.all().delete()
        for ingredient in ingredients_values:
            IngredientRecipe.objects.create(
                recipe=instance,
                amount=ingredient['amount'],
                ingredient=Ingredient.objects.get(
                    id=ingredient['id']
                )
            )
        instance.save()
        return instance
