# Thirdparty imports
from django.contrib import admin
from django.contrib.auth import get_user_model

# Projects imports
from .forms import RecipeForm
from .models import Ingredient, Recipe, Tag

User = get_user_model()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm
    list_display = ('name', 'author')
    search_fields = ('name', 'author__username')
