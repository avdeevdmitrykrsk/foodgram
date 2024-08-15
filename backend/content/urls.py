# Thirdparty imports
from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# Projects imports
from content.views import (DownloadShoppingCartView, FavoriteViewSet,
                           IngredientsViewSet, RecipesViewSet,
                           ShoppingCartViewSet, ShortLinkView, TagViewSet)

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path(
        'recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'recipes/<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view(
            {
                'get': 'retrieve',
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'recipes/download_shopping_cart/', DownloadShoppingCartView.as_view()
    ),
    path('recipes/<int:pk>/get-link/', ShortLinkView.as_view()),
    path('', include(router.urls)),
]
