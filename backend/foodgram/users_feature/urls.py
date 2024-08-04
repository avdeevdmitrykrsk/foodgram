from django.urls import path

from users_feature.views import (
    FavoriteViewSet, SubscribeToUser, SubscriptionsViewSet
)

urlpatterns = [
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
    path('recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
        {
            'post': 'create',
            'delete': 'destroy'
        }
    ))
]
