from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from users_feature.models import Subscribe
from users_feature.serializers import SubscribeSerializer, Subscriptions

User = get_user_model()


class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Subscriptions

    def get_queryset(self):
        print(self.request.user.subscribe_list_by_user.all())
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
