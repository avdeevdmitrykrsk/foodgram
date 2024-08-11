# Projects imports
from users.utils import check_list
from users_feature.models import Subscribe


def check_subscribe(request, obj):
    subscribe_list = Subscribe.objects.filter(
        user=request.user
    )
    return check_list(obj, subscribe_list, 'subscribe_to')
