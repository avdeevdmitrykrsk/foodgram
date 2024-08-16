# Thirdparty imports
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# Projects imports
from users.views import (AvatarViewSet, FoodgramUserViewSet, MeViewSet,
                         SubscriptionsViewSet)

router = DefaultRouter()
router.register('users', FoodgramUserViewSet, basename='users')

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
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
