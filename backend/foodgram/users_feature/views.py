# Thirdparty imports
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import FileResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

# Projects imports
from content.models import Recipe
from users_feature.models import Favorite, ShoppingCart, Subscribe
from users_feature.paginations import PaginateByPageLimit
from users_feature.serializers import (FavoriteSerializer,
                                       ShoppingCartSerializer,
                                       SubscribeSerializer, Subscriptions)
from users_feature.utils import check_subscribe

User = get_user_model()

INGREDIENT_POS = 0
MEASUREMENT_UNIT_POS = 1


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        if not Recipe.objects.filter(
            id=recipe_id
        ).exists():
            print('sadf')
            return Response(
                data={'detail': 'Страница не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.user.cart_by_user.filter(
            recipe_id=recipe_id
        ).exists():
            raise ValidationError(
                'Данный рецепт уже в списке покупок.'
            )
        cart = ShoppingCart.objects.create(
            user=request.user,
            recipe=Recipe.objects.get(
                id=recipe_id
            )
        )
        cart_data = {
            'id': cart.recipe.id,
            'name': cart.recipe.name,
            'image': cart.recipe.image.url,
            'cooking_time': cart.recipe.cooking_time
        }
        return Response(data=cart_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        if not Recipe.objects.filter(id=recipe_id).exists():
            return Response(
                data={'detail': 'Страница не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            recipe_id = kwargs.get('pk')
            request.user.cart_by_user.get(
                recipe_id=recipe_id
            ).delete()
        except ObjectDoesNotExist:
            raise ValidationError(
                'Данного рецепта не существует в корзине.'
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartView(APIView):

    def get(self, request, *args, **kwargs):
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
        with open('shopping_cart.txt', 'w', encoding='utf-8') as f:
            for values in ingredients_count:
                ingredient, value, mes_unit = values
                f.write(f'{ingredient} = {value}{mes_unit}\n')
        return FileResponse(open('shopping_cart.txt', 'rb'))


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        me_user = request.user
        recipe_id = kwargs.get('pk')
        if not Recipe.objects.filter(id=recipe_id):
            return Response(
                data={'detail': 'Страница не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if me_user.favorite_list_by_user.filter(
            recipe_id=recipe_id
        ).exists():
            raise ValidationError(
                'Данный рецепт уже в списке избранных рецептов.'
            )
        favorite = Favorite.objects.create(
            user=me_user,
            recipe=Recipe.objects.get(
                id=recipe_id
            )
        )
        favorite_data = {
            'id': favorite.recipe.id,
            'name': favorite.recipe.name,
            'image': favorite.recipe.image.url,
            'cooking_time': favorite.recipe.cooking_time
        }
        return Response(data=favorite_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs.get('pk')
        if not Recipe.objects.filter(id=recipe_id).exists():
            return Response(
                data={'detail': 'Страница не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            recipe_id = kwargs.get('pk')
            request.user.favorite_list_by_user.get(
                recipe_id=recipe_id
            ).delete()
        except ObjectDoesNotExist:
            raise ValidationError(
                'Данного рецепта не существует в избранных.'
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = Subscriptions
    pagination_class = PaginateByPageLimit
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return [
            sub.subscribe_to for sub in (
                self.request.user.subscribe_list_by_user.all()
            )
        ]


class SubscribeToUser(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_recipes_count(self, request, obj):
        return len(self.get_recipes(request, obj))

    @staticmethod
    def get_recipes(request, obj):
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.recipe_set.all()
        if recipes_limit:
            recipes = obj.recipe_set.all()[:int(recipes_limit)]
        return recipes.values(
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def create(self, request, *args, **kwargs):
        me_user = request.user
        sub_user_id = kwargs.get('pk')
        if not User.objects.filter(id=sub_user_id).exists():
            return Response(
                data={'detail': 'Страница не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )
        sub_user = User.objects.get(id=sub_user_id)
        if me_user.subscribe_list_by_user.filter(
            subscribe_to_id=sub_user_id
        ).exists():
            raise ValidationError(
                'Данный пользователь уже в списке ваших подписок.'
            )
        if me_user == sub_user:
            raise ValidationError('Нельзя подписываться на себя.')
        subscribe = Subscribe.objects.create(
            user=me_user, subscribe_to=sub_user
        )
        try:
            avatar = subscribe.subscribe_to.avatar.url
        except ValueError:
            avatar = None
        subscribe_data = {
            'email': subscribe.subscribe_to.email,
            'id': subscribe.subscribe_to.id,
            'username': subscribe.subscribe_to.username,
            'first_name': subscribe.subscribe_to.first_name,
            'last_name': subscribe.subscribe_to.last_name,
            'is_subscribed': check_subscribe(request, sub_user),
            'recipes': self.get_recipes(request, sub_user),
            'recipes_count': self.get_recipes_count(self, request, sub_user),
            'avatar': avatar
        }
        return Response(data=subscribe_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if not User.objects.filter(id=user_id).exists():
            return Response(
                data={'detail': 'Страница не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            request.user.subscribe_list_by_user.get(
                subscribe_to_id=user_id
            ).delete()
        except ObjectDoesNotExist:
            raise ValidationError(
                'Данного пользователя не существует в ваших подписках.'
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
