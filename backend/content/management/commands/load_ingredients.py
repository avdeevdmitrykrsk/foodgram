# Standart lib imports
import csv
import os

# Thirdparty imports
from content.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание иингредиентов.'

    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..', '..', '..', '..', 'data'
            )
        )
        file_path = os.path.join(data_folder, 'ingredients.csv')
        with open(
            file_path,
            'r', encoding='utf-8'
        ) as f:
            ingredients = csv.reader(f)
            for ingredient in ingredients:
                name, mes = ingredient
                Ingredient.objects.create(name=name, measurement_unit=mes)
        self.stdout.write(
            self.style.SUCCESS('Ингредиенты импортированы в БД.')
        )
