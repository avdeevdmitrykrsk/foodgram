# Thirdparty imports
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

# Projects imports
from content.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from users.fields import Base64ToImage
from users.serializers import UserSerializer

EXPECTED_RECIPE_FIELDS = (
    'ingredients', 'tags', 'name', 'text', 'cooking_time'
)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class GetRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(
        read_only=True, many=True
    )
    author = UserSerializer(read_only=True)
    image = Base64ToImage()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('get_ingredient_recipe__amount')
        )


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ToImage()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags',
            'image', 'name', 'text', 'cooking_time'
        )
        extra_kwargs = {
            'tags': {'required': True},
            'ingredients': {'required': True},
            'image': {'required': True},
            'name': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True}
        }

    def validate_tags(self, value):
        if len(value) != len(set(value)):
            raise ValidationError(
                'Не должно быть одинаковых Тэгов.'
            )
        return value

    def validate_ingredients(self, value):
        values_id = [
            ingredient['id'] for ingredient in value
        ]
        if len(values_id) != len(set(values_id)):
            raise ValidationError(
                'Не должно быть одинаковых Ингредиентов.'
            )
        return value

    def validate_image(self, value):
        if not value:
            raise ValidationError('image не был указан.')
        return value

    def validate(self, attrs):
        for field in EXPECTED_RECIPE_FIELDS:
            if not attrs.get(field):
                raise ValidationError(f'{field} не был указан.')
        return attrs

    def to_representation(self, instance):
        serializer = GetRecipeSerializer(instance)
        return serializer.data

    def ingredientrecipe_create(self, ingredients, recipe):
        for value in ingredients:
            ingredient, amount = value.values()
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=amount,
                ingredient=Ingredient.objects.get(
                    id=ingredient.id
                )
            )

    @transaction.atomic
    def create(self, validated_data):
        tags_values = validated_data.pop('tags')
        ingredients_values = validated_data.pop('ingredients')

        instance = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )

        instance.tags.set(tags_values)
        self.ingredientrecipe_create(ingredients_values, instance)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        tags_values = validated_data.pop('tags')
        instance.tags.set(tags_values)

        ingredients_values = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.ingredientrecipe_create(ingredients_values, instance)
        return super().update(instance, validated_data)


class FavoriteShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'recipe',)

    def validate_recipe(self, value):
        get_object_or_404(Recipe, id=value.id)
        return value


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta(FavoriteShoppingCartSerializer.Meta):
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta(FavoriteShoppingCartSerializer.Meta):
        model = ShoppingCart
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe')
            )
        ]
