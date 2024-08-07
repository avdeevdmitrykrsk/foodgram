from django.db.models import F
from rest_framework import serializers

from content.models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
)
from users.serializers import UserSerializer
from users.utils import Base64ToAvatar, check_list
from users_feature.models import Favorite, ShoppingCart


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class GetRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(method_name='make_data')
    tags = TagSerializer(read_only=True, many=True)
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
        shopping_cart_list = ShoppingCart.objects.filter(
            user=self.context.get('request').user
        )
        return check_list(obj, shopping_cart_list, 'recipe')

    def check_favorite(self, obj):
        favorite_list = Favorite.objects.filter(
            user=self.context.get('request').user
        )
        return check_list(obj, favorite_list, 'recipe')

    def make_data(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredientrecipe__amount')
        )


# class IngredientAmountSerializer(serializers.ModelSerializer):
#     id = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )

#     class Meta:
#         model = IngredientRecipe
#         fields = ('id', 'amount')


class RecipeSerializer(GetRecipeSerializer):

    class Meta(GetRecipeSerializer.Meta):
        read_only_fields = (
            'tags', 'ingredients', 'author'
        )

    def create(self, validated_data):
        tags_values = self.initial_data.pop('tags')
        ingredients_values = self.initial_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
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
        instance.ingredientrecipe_set.all().delete()
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
