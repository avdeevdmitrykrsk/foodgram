from django.urls import include, path
from rest_framework.routers import DefaultRouter

from content.views import (
    IngredientsViewSet, RecipesViewSet, ShortLinkView, TagViewSet
)

router = DefaultRouter()
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/<int:pk>/get-link/', ShortLinkView.as_view()),
    path('', include(router.urls)),
]
