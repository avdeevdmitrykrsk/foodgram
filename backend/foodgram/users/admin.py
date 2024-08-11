# Thirdparty imports
from django.contrib import admin
from django.contrib.auth import get_user_model

# Projects imports
from .models import FoodgramUser

User = get_user_model()


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name',
        'last_name', 'email', 'avatar'
    )
    search_fields = ('username', 'email')
