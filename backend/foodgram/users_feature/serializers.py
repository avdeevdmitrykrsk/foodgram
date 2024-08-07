from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import F
from rest_framework import serializers

from content.models import Recipe
from users.utils import Base64ToAvatar, check_list
from users_feature.models import Favorite, Subscribe, ShoppingCart
from users_feature.utils import add_recipe_to_list

User = get_user_model()


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('recipe',)
        read_only_fields = ('recipe',)

    def create(self, validated_data):
        return add_recipe_to_list(self, Recipe)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe',)
        read_only_fields = ('recipe',)

    def create(self, validated_data):
        return add_recipe_to_list(self, Recipe)


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('user', 'subscribe')
        extra_kwargs = {
            'user': {'write_only': True, 'required': False},
            'subscribe': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        me_user = self.context.get('request').user
        sub_user_id = self.context.get(
            'request'
        ).parser_context['kwargs']['pk']
        sub_user = User.objects.get(id=sub_user_id)
        if me_user == sub_user:
            raise ValidationError('Нельзя подписываться на себя любимого! ;)')
        return Subscribe.objects.create(user=me_user, subscribe=sub_user)


class Subscriptions(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='check_subscribe'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'avatar',
        )
        read_only_fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar',
        )

    def check_subscribe(self, obj):
        subscribe_list = Subscribe.objects.filter(
            user=self.context.get('request').user
        )
        return check_list(obj, subscribe_list, Subscribe)

    def get_recipes(self, obj):
        recipes = obj.recipe_set.all()
        return recipes.values(
            'id',
            'name',
            'image',
            'cooking_time'
        )
