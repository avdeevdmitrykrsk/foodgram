# Thirdparty imports
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# Projects imports
from content.models import Recipe
from users.fields import Base64ToImage
from users.models import Subscribe

User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ToImage()

    class Meta:
        model = User
        fields = ('avatar',)

    @transaction.atomic
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
        request = self.context.get('request')
        return bool(
            request
            and request.user.is_authenticated
            and obj in Subscribe.objects.filter(
                user=request.user, subscribe_to=obj
            )
        )


class GetUserRecipes(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class Subscriptions(UserSerializer):
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count', 'avatar',
        )
        read_only_fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar',
        )

    def get_recipes_count(self, obj):
        return obj.recipes_by_author.all().count()

    def get_recipes(self, obj):
        query_params = self.context.get('request').query_params
        recipes = obj.recipes_by_author.all()
        recipes_limit = query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = GetUserRecipes(recipes, many=True)
        return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('user', 'subscribe_to')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'subscribe_to')
            )
        ]

    def validate_subscribe_to(self, value):
        request = self.context.get('request')
        if request.user == value:
            raise serializers.ValidationError(
                'Нельзя подписывать на себя.'
            )
        return value
