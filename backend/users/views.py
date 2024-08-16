# Thirdparty imports
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

# Projects imports
from content.paginations import PaginateByPageLimit
from users.serializers import (AvatarSerializer, SubscribeSerializer,
                               Subscriptions, UserSerializer)

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
        user = self.request.user
        return User.objects.get_annotated_queryset(user).filter(
            subscribe_list_by_subscribe_to__user=user
        )


class FoodgramUserViewSet(UserViewSet):
    pagination_class = PaginateByPageLimit

    def get_queryset(self):
        return User.objects.get_annotated_queryset(self.request.user)

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='subscribe',
        permission_classes=(IsAuthenticated,)
    )
    def subscribe_to_user(self, request, *args, **kwargs):
        if request.method == 'POST':
            sub_user_id = kwargs.get('id')
            sub_user = get_object_or_404(User, id=sub_user_id)
            data = {
                'user': request.user.id,
                'subscribe_to': sub_user_id
            }
            context = self.get_serializer_context()
            serializer = SubscribeSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = Subscriptions(sub_user, context=context)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            get_object_or_404(User, id=kwargs.get('id'))
            instance = request.user.subscribe_list_by_user.filter(
                subscribe_to__id=kwargs.get('id')
            )
            count, _ = instance.delete()
            if not count:
                raise ValidationError(
                    'Пользователя с данным id нет в списке ваших подписок.'
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
