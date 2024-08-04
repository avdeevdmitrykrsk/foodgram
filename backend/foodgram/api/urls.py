from django.urls import include, path

urlpatterns = [
    path('', include('users.urls')),
    path('', include('content.urls')),
    path('', include('users_feature.urls'))
]
