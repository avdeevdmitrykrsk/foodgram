# Thirdparty imports
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

# Projects imports
from content.models import Recipe
from users.serializers import GetUserRecipes


def delete_favorite_shopping_cart(request, serializer_class, pk):
    get_object_or_404(Recipe, id=pk)
    instance = serializer_class.objects.filter(
        user=request.user, recipe_id=pk
    )
    count, _ = instance.delete()
    if not count:
        raise ValidationError(
            'Рецепт отсутствует в списке '
            f'\'{instance.model._meta.verbose_name}\'.'
        )
    return Response(status=status.HTTP_204_NO_CONTENT)


def create_favorite_shopping_cart(request, serializer_class, pk):
    instance = get_object_or_404(Recipe, id=pk)
    data = {
        'user': request.user.id,
        'recipe': instance.id
    }
    serializer = serializer_class(data=data, context=request.parser_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    serializer = GetUserRecipes(instance)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)
