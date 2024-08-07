import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


def check_list(obj, obj_list, sub_model):
    for value in obj_list:
        if obj == getattr(value, sub_model, None):
            return True
    return False


class Base64ToAvatar(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
