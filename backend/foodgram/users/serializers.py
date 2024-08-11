# Thirdparty imports
from django.contrib.auth import get_user_model
from rest_framework import serializers

# Projects imports
from users.utils import Base64ToAvatar, check_list
from users_feature.models import Subscribe

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
        user = self.context.get('request').user
        if user.is_authenticated:
            subscribe_list = Subscribe.objects.filter(
                user=user
            )
            return check_list(obj, subscribe_list, 'subscribe')
        return False


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password'
        )
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    # def validate_username(self, username):
    #     if not re.match(r'^[\w.@+-]+\z', username):
    #         raise ValidationError('Неподходящий юзернейм.')
    #     return username

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
