# Generated by Django 3.2.3 on 2024-08-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_subscribe_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodgramuser',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='foodgramuser',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last_name'),
        ),
    ]
