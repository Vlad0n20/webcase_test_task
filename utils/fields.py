import os.path

from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from rest_framework import serializers

from utils.uploaded_file import resize_image


class ChoicesField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choice_strings_to_display = {
            key: value for key, value in self.choices.items()
        }

    def to_representation(self, value):
        if value in ('', None):
            return value
        return {
            'value': self.choice_strings_to_values.get(value, value),
            'display': self.choice_strings_to_display.get(value, value),
        }


class AvatarField(serializers.ImageField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        resize_image(data.temporary_file_path(), 81, 81)
        return data

    def to_representation(self, value):
        if not value:
            return None
        url = settings.UPLOAD_DIR['media'] + '/'.join([value.instance.__class__.__name__.lower(),
                        str(value.instance.pk),
                        os.path.basename(value.name)])
        return url
