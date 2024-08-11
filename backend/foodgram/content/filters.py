from django_filters import rest_framework as filter
from rest_framework.filters import BaseFilterBackend

from content.models import Ingredient


class IngredientNameFilterBackend(filter.FilterSet):
    name = filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']


class AuthorFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_params = request.query_params
        if 'author' in filter_params:
            author_id = filter_params.get('author')
            return queryset.filter(author_id=author_id)
        return queryset


class IsFavoritedFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            filter_params = request.query_params
            if 'is_favorited' in filter_params:
                return queryset.filter(
                    favorite_list_by_recipe__user=request.user
                )
        return queryset


class ShoppingCartFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            filter_params = request.query_params
            if 'is_in_shopping_cart' in filter_params:
                return queryset.filter(
                    cart_list_by_recipe__user=request.user
                )
        return queryset


class TagFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_params = request.query_params
        if 'tags' in filter_params:
            tags = filter_params.getlist('tags')
            return queryset.filter(
                tags__slug__in=tags
            ).distinct()
        return queryset
