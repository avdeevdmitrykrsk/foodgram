# Thirdparty imports
from django.urls import include, path

# Projects imports
from users.views import (AvatarViewSet, MeViewSet, SubscribeToUser,
                         SubscriptionsViewSet)

urlpatterns = [
    path(
        'users/me/', MeViewSet.as_view(
            {
                'get': 'retrieve'
            }
        )
    ),
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
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
