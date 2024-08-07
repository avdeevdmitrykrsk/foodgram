from django.urls import include, path

urlpatterns = [
    path('', include('users_feature.urls')),
    path('', include('users.urls')),
    path('', include('content.urls'))
]
