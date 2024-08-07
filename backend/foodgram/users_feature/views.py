from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Q, F
from django.http import FileResponse
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from content.models import Recipe, IngredientRecipe
from users_feature.models import Favorite, Subscribe, ShoppingCart
from users_feature.serializers import (
    FavoriteSerializer, SubscribeSerializer,
    Subscriptions, ShoppingCartSerializer
)

User = get_user_model()

INGREDIENT_POS = 0
MEASUREMENT_UNIT_POS = 1


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_object(self):
        return ShoppingCart.objects.get(
            recipe_id=self.request.parser_context['kwargs']['pk']
        )

    def perform_create(self, request, *args, **kwargs):
        return ShoppingCart.objects.create(
            user=self.request.user,
            recipe=Recipe.objects.get(
                id=self.request.parser_context['kwargs']['pk']
            )
        )


class DownloadShoppingCartView(APIView):

    def get(self, request, *args, **kwargs):
        # FileResponse
        my_recipes = ShoppingCart.objects.filter(
            user=request.user
        )
        ingredients_count = []
        ingredients_list = []
        for rec in my_recipes:
            for ingredients in rec.recipe.ingredientrecipe_set.all():
                ingredients_list.append(
                    (
                        getattr(
                            ingredients, 'ingredient'
                        ).name,
                        getattr(
                            ingredients, 'ingredient'
                        ).measurement_unit.strip()
                    )
                )
        for ingredient in ingredients_list:
            ingredient_count = my_recipes.filter(
                recipe__ingredientrecipe__ingredient__name=ingredient[0]
            ).aggregate(count=Sum('recipe__ingredientrecipe__amount'))
            ingredients_count.append(
                (
                    ingredient[INGREDIENT_POS],
                    ingredient_count['count'],
                    ingredient[MEASUREMENT_UNIT_POS]
                )
            )
        ingredients_count = list(set(ingredients_count))
        print(ingredients_count)
        with open('shopping_cart.txt', 'w', encoding='utf-8') as f:
            for values in ingredients_count:
                ingredient, value, mes_unit = values
                f.write(f'{ingredient} = {value}{mes_unit}\n')
        return FileResponse(open('shopping_cart.txt', 'rb'))


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_object(self):
        return Favorite.objects.get(
            recipe_id=self.request.parser_context['kwargs']['pk']
        )

    def perform_create(self, request, *args, **kwargs):
        return Favorite.objects.create(
            user=self.request.user,
            recipe=Recipe.objects.get(
                id=self.request.parser_context['kwargs']['pk']
            )
        )


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Subscriptions

    def get_queryset(self):
        return [
            sub.subscribe_to for sub in (
                self.request.user.subscribe_list_by_user.all()
            )
        ]


class SubscribeToUser(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (AllowAny,)

    # def get_serializer_class(self):
    #     return self.serializer_class if (
    #         self.request.method == 'POST'
    #     ) else Subscriptions
