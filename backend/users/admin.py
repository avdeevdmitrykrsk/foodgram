# Thirdparty imports
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django_short_url.models import ShortURL
from rest_framework.authtoken.models import TokenProxy

# Projects imports
from .models import FoodgramUser

User = get_user_model()

admin.site.unregister(Group)
admin.site.unregister(ShortURL)
admin.site.unregister(TokenProxy)


@admin.register(FoodgramUser)
class FoodgramUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name',
        'last_name', 'email', 'avatar'
    )
    search_fields = ('username', 'email')
