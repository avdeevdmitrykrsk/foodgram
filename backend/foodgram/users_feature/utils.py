# Projects imports
from users.utils import check_list
from users_feature.models import Subscribe


def make_recipe_data(obj):
    return {
        'id': obj.recipe.id,
        'name': obj.recipe.name,
        'image': obj.recipe.image.url,
        'cooking_time': obj.recipe.cooking_time
    }


def check_subscribe(request, obj):
    subscribe_list = Subscribe.objects.filter(
        user=request.user
    )
    return check_list(obj, subscribe_list, 'subscribe_to')
