# Thirdparty imports
from django.contrib.auth import get_user_model
from rest_framework import serializers

# Projects imports
from users.utils import check_list
from users_feature.models import Favorite, ShoppingCart, Subscribe

User = get_user_model()


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('recipe',)
        read_only_fields = ('recipe',)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe',)
        read_only_fields = ('recipe',)


class Subscriptions(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='check_subscribe'
    )
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

    def check_subscribe(self, obj):
        subscribe_list = Subscribe.objects.filter(
            user=self.context.get('request').user
        )
        return check_list(obj, subscribe_list, 'subscribe')

    def get_recipes_count(self, obj):
        return len(self.get_recipes(obj))

    def get_recipes(self, obj):
        recipes_limit = self.context.get(
            'request', None
        ).query_params.get('recipes_limit')
        recipes = obj.recipe_set.all()
        if recipes_limit:
            recipes = obj.recipe_set.all()[:int(recipes_limit)]
        return recipes.values(
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribeSerializer(serializers.ModelSerializer):
    user = Subscriptions(required=False)

    class Meta:
        model = Subscribe
        fields = ('user',)
        extra_kwargs = {
            'user': {'required': False},
            'subscribe_to': {'write_only': True, 'required': False}
        }
