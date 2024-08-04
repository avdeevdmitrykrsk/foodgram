from django.urls import include, path

from users.views import AvatarViewSet

urlpatterns = [
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
