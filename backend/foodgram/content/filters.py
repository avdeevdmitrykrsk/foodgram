from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class AuthorFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_params = request.query_params
        if 'author' in filter_params:
            author_id = filter_params.get('author')
            return queryset.model.objects.filter(author_id=author_id)
        return queryset


class IsFavoritedFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        print(queryset)
        filter_params = request.query_params
        if 'is_favorited' in filter_params:
            return queryset.filter(
                favorite__user=request.user
            ).prefetch_related('favorite_set')
        return queryset


class ShoppingCartFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_params = request.query_params
        if 'is_in_shopping_cart' in filter_params:
            return queryset.filter(
                shoppingcart__user=request.user
            ).prefetch_related('shoppingcart_set')
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
