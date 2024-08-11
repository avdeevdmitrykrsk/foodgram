# Thirdparty imports
from django import forms

# Projects imports
from .models import Recipe


class RecipeForm(forms.ModelForm):
    favorite_count = forms.IntegerField(
        required=False,
        label='Добавили в избранное',
        widget=forms.NumberInput(
            attrs={'readonly': 'readonly'}
        )
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time', 'favorite_count'
        )
        read_only_fields = ('author', 'favorite_count',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['favorite_count'] = (
                self.instance.favorite_list_by_recipe.count()
            )
