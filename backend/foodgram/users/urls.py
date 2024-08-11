# Thirdparty imports
from django.urls import include, path

# Projects imports
from users.views import AvatarViewSet, MeViewSet

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
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
