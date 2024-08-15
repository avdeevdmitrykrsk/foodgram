# Thirdparty imports
import re
from django.db import transaction
from django.db.models import Exists, OuterRef, Sum
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from rest_framework import status, views, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

# Projects imports
from content.crud_for_favorite_shopping_cart import (
    create_favorite_shopping_cart, delete_favorite_shopping_cart)
from content.filters import IngredientNameFilterBackend, RecipeFilter
from content.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from content.paginations import PaginateByPageLimit
from content.permissions import IsAuthorOrReadOnly
from content.serializers import (FavoriteSerializer, GetRecipeSerializer,
                                 IngredientSerializer, RecipeSerializer,
                                 ShoppingCartSerializer, TagSerializer)

SURL_URL_POS = 2
LURL_URL_POS = 0
SAFE_ACTIONS = ('list', 'retrieve')


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return create_favorite_shopping_cart(
            request, ShoppingCartSerializer, kwargs.get('pk')
        )

    def destroy(self, request, *args, **kwargs):
        return delete_favorite_shopping_cart(
            request, ShoppingCart, kwargs.get('pk')
        )


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return create_favorite_shopping_cart(
            request, FavoriteSerializer, kwargs.get('pk')
        )

    def destroy(self, request, *args, **kwargs):
        return delete_favorite_shopping_cart(
            request, Favorite, kwargs.get('pk')
        )


class ShortLinkView(views.APIView):

    def get(self, request, *args, **kwargs):
        if re.match(r'^\/s\/[\w]{3}\/', request.path):
            surl = request.path.split('/')
            lurl = ShortURL.objects.get(surl=surl[SURL_URL_POS]).lurl
            return redirect(lurl)

        lurl = request.path.split('get-link/')[LURL_URL_POS]
        surl = get_surl(lurl)
        path = f'{request.get_host()}{surl}'
        data = {
            'short-link': path
        }
        return Response(data=data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = PaginateByPageLimit
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.annotate(
                is_favorited=Exists(
                    Favorite.objects.filter(
                        user=self.request.user, recipe=OuterRef('pk')
                    )
                ),
                is_in_shopping_cart=Exists(
                    ShoppingCart.objects.filter(
                        user=self.request.user, recipe=OuterRef('pk')
                    )
                ),
            ).order_by('name', 'author')
        return Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in SAFE_ACTIONS:
            return GetRecipeSerializer
        return RecipeSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientNameFilterBackend
    http_method_names = ('get',)
    pagination_class = None


class DownloadShoppingCartView(APIView):

    def get(self, request, *args, **kwargs):
        cart_data = IngredientRecipe.objects.filter(
            recipe__shopping_cart_list__user=request.user
        ).values('ingredient__name').annotate(
            amount=Sum('amount')
        ).order_by('ingredient__name')

        response = Response(cart_data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping.txt"'
        return response
