import uuid

from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import magic

from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat


def parse_int(value):
    """ Return the value casted to integer, or None if casting is not possible.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_bool(value):
    return value in [1, "1", 'true', 't', 'True']


def parse_uuid(value):
    """ Return the value casted to UUID, or NOne if casting is not possible
    """
    try:
        return uuid.UUID(value)
    except (TypeError, ValueError):
        return None


def float_or_as_is(value):
    """ Return value casted to float or the original value, if the cast is impossible
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


phone_regex = RegexValidator(regex=r'^\+\d{9,15}$',
                             message=_("The phone number must be entered in the format: "
                                       "'+999999999'. Up to 15 digits allowed."))


def validate_ids(data, field="id", unique=True):
    if isinstance(data, list):
        id_list = [int(x[field]) for x in data]

        if unique and len(id_list) != len(set(id_list)):
            raise ValidationError("Multiple updates to a single {} found".format(field))

        return id_list

    return [data]


class UpdateListSerializer(serializers.ListSerializer):

    def update(self, instances, validated_data):
        instance_hash = {index: instance for index, instance in enumerate(instances)}
        if len(instance_hash) == 0:
            return []
        print(len(instance_hash), len(validated_data))

        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]

        return result


class FileValidator(object):
    error_messages = {
        'max_size': "Ensure this file size is not greater than %(max_size)s."
                    " Your file size is %(size)s.",
        'min_size': "Ensure this file size is not less than %(min_size)s. "
                    "Your file size is %(size)s.",
        'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'] % params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'] % params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if (not (content_type == 'application/zip' and (data.name.endswith('.docx') or data.name.endswith('.xlsx')))
                    and content_type not in self.content_types):
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'] % params)

    def __eq__(self, other):
        return (
                isinstance(other, FileValidator) and
                self.max_size == other.max_size and
                self.min_size == other.min_size and
                self.content_types == other.content_types
        )


avatar_validator = FileValidator(max_size=10485760,
                                 content_types=('image/jpeg', 'image/png'))

file_validator = FileValidator(
    max_size=52428800,
    content_types=(
        'image/jpeg',
        'image/png',
        'application/pdf',
        'image/gif',
        'text/csv',
        'video/mpeg',
        'video/mp4',
        'application/vnd.oasis.opendocument.text',
        'application/vnd.oasis.opendocument.spreadsheet',
        'application/vnd.oasis.opendocument.presentation',
        'application/vnd.oasis.opendocument.graphics',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'audio/mpeg',
        'image/heic',
        'image/heif',
        'application/msword',  # Microsoft Word (.doc)
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # Word (.docx)
    )
)
