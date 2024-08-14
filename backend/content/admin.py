# Thirdparty imports
from typing import Any
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count

# Projects imports
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


class IngredientInline(admin.StackedInline):
    model = Recipe.ingredients.through
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author__username', 'tags__slug')
    fields = (
        'name', 'tags', 'text', 'image',
        'cooking_time', 'author', 'get_favorite_count'
    )
    readonly_fields = ('get_favorite_count', 'author')
    inlines = [IngredientInline]


    @admin.display(description='В избранном у')
    def get_favorite_count(self, obj):
        return str(
            obj.favorite_list.all().count()
        )
