from django.db.models import Count, F
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend, SearchFilter
from rest_framework.permissions import AllowAny

from content.models import Ingredient, IngredientRecipe, Recipe, Tag
from content.serializers import (
    GetRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)
    pagination_class = None


class IsFavoritedFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_param = request.query_params.get('is_favorited', None)
        if filter_param:
            queryset = [
                rec.recipe for rec in request.user.favorite_list_by_user.all()
            ]
        return queryset


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (SearchFilter, IsFavoritedFilterBackend)
    search_fields = ('ingredients', 'tags',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return GetRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
    # http_method_names = ('get', 'post', 'patch', 'delete')

