from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models import F
from rest_framework import serializers

from users_feature.models import Subscribe
from users.utils import Base64ToAvatar

User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ToAvatar()

    class Meta:
        model = User
        fields = ('avatar',)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='check_subscribe'
    )

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar',
        ]
        read_only_fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar',
        )

    def check_subscribe(self, obj):
        me_user = self.context.get('request').user
        subscribe_list = Subscribe.objects.filter(user=me_user)
        for sub in subscribe_list:
            if obj == sub.subscribe:
                return True
        return False


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
