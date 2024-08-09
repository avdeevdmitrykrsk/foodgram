# Generated by Django 3.2.3 on 2024-08-09 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_remove_recipe_short_link_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount_by_ingredient', to='content.ingredient', verbose_name='Ингредиент'),
        ),
    ]
