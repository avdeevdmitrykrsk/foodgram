from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from content.models import Recipe
from users_feature.models import Subscribe, Favorite
from users_feature.serializers import (
    SubscribeSerializer, Subscriptions, FavoriteSerializer
)

User = get_user_model()


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_object(self):
        return Favorite.objects.get(
            recipe_id=self.request.parser_context['kwargs']['pk']
        )

    def perform_create(self, request, *args, **kwargs):
        # self.create
        return Favorite.objects.create(
            user=self.request.user,
            recipe=Recipe.objects.get(
                id=self.request.parser_context['kwargs']['pk']
            )
        )


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Subscriptions

    def get_queryset(self):
        return [
            sub.subscribe_to for sub in (
                self.request.user.subscribe_list_by_user.all()
            )
        ]


class SubscribeToUser(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (AllowAny,)

    # def get_serializer_class(self):
    #     return self.serializer_class if (
    #         self.request.method == 'POST'
    #     ) else Subscriptions
