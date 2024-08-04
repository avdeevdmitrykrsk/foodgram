from django.urls import include, path

from users.views import AvatarViewSet
from users_feature.views import SubscribeToUser, SubscriptionsViewSet

urlpatterns = [
    path(
        'users/me/avatar/', AvatarViewSet.as_view(
            {
                'put': 'update',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'users/subscriptions/', SubscriptionsViewSet.as_view(
            {
                'get': 'list'
            }
        )
    ),
    path(
        'users/<int:pk>/subscribe/', SubscribeToUser.as_view(
            {
                'post': 'create'
            }
        )
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
