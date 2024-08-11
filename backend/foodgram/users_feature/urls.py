# Thirdparty imports
from django.urls import path

# Projects imports
from users_feature.views import (DownloadShoppingCartView, FavoriteViewSet,
                                 ShoppingCartViewSet, SubscribeToUser,
                                 SubscriptionsViewSet)

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
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'recipes/<int:pk>/favorite/', FavoriteViewSet.as_view(
            {
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'recipes/<int:pk>/shopping_cart/', ShoppingCartViewSet.as_view(
            {
                'get': 'retrieve',
                'post': 'create',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'recipes/download_shopping_cart/', DownloadShoppingCartView.as_view()
    )
]
