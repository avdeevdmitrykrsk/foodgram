# Thirdparty imports
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

# Projects imports
from content.models import Recipe
from content.paginations import PaginateByPageLimit
from users.models import Subscribe
from users.serializers import (AvatarSerializer, SubscribeSerializer,
                               Subscriptions, UserSerializer)
# from users.utils import make_recipe_data

User = get_user_model()


class MeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AvatarSerializer
    http_method_names = ('put', 'delete')
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        self.get_object().avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = Subscriptions
    pagination_class = PaginateByPageLimit
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(
            subscribe_list_by_subscribe_to__user=self.request.user
        )


class SubscribeToUser(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        sub_user_id = kwargs.get('pk')
        sub_user = get_object_or_404(User, id=sub_user_id)
        if request.user.subscribe_list_by_user.filter(
            subscribe_to__id=sub_user_id
        ).exists():
            raise ValidationError(
                'Данный пользователь уже в списке ваших подписок.'
            )
        if request.user == sub_user:
            raise ValidationError('Нельзя подписываться на себя.')
        data = {
            'user': request.user.id,
            'subscribe_to': sub_user_id
        }
        context = self.get_serializer_context()
        serializer = SubscribeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = Subscriptions(sub_user, context=context)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(User, id=kwargs.get('pk'))
        instance = request.user.subscribe_list_by_user.filter(
            subscribe_to__id=kwargs.get('pk')
        )
        count, _ = instance.delete()
        if not count:
            raise ValidationError(
                'Пользователя с данным id нет в списке ваших подписок.'
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
