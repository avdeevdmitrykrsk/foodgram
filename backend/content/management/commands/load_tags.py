# Standart lib imports
import csv
import os

# Thirdparty imports
from content.models import Tag
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание тэгов.'

    def handle(self, *args, **kwargs):
        data_folder = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..', '..', '..', '..', 'data'
            )
        )
        file_path = os.path.join(data_folder, 'tags.csv')
        with open(
            file_path,
            'r', encoding='utf-8'
        ) as f:
            tags = csv.reader(f)
            for tag in tags:
                name, slug = tag
                Tag.objects.create(name=name, slug=slug)
        self.stdout.write(
            self.style.SUCCESS('Тэги импортированы в БД.')
        )
