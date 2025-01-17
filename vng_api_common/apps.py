from django.apps import AppConfig
from django.db import models

from drf_yasg import openapi
from drf_yasg.inspectors.field import (
    basic_type_info,
    model_field_to_basic_type,
    serializer_field_to_basic_type,
)
from rest_framework import serializers

from . import fields
from .serializers import DurationField

try:
    from relativedeltafield import RelativeDeltaField
except ImportError:
    RelativeDeltaField = None

# https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#data-types
# and https://github.com/OAI/OpenAPI-Specification/issues/845 - format: duration
# is collected somewhere so there's precedent
FORMAT_DURATION = "duration"


class ZDSSchemaConfig(AppConfig):
    name = "vng_api_common"

    def ready(self):
        from . import checks  # noqa

        patch_duration_type()
        register_serializer_field()


def patch_duration_type():
    def _patch(basic_types, _field_cls, format=None):
        for index, (field_cls, basic_type) in enumerate(basic_types):
            if field_cls is _field_cls:
                basic_types[index] = (_field_cls, (openapi.TYPE_STRING, format))
                break

    _patch(model_field_to_basic_type, models.DurationField, FORMAT_DURATION)
    _patch(basic_type_info, models.DurationField, FORMAT_DURATION)
    _patch(serializer_field_to_basic_type, serializers.DurationField, FORMAT_DURATION)
    _patch(basic_type_info, serializers.DurationField, FORMAT_DURATION)

    # best-effort support for relativedeltafield
    if RelativeDeltaField is not None:
        _patch(model_field_to_basic_type, RelativeDeltaField, FORMAT_DURATION)
        _patch(basic_type_info, RelativeDeltaField, FORMAT_DURATION)


def register_serializer_field():
    mapping = serializers.ModelSerializer.serializer_field_mapping
    mapping[models.fields.DurationField] = DurationField
    mapping[fields.DaysDurationField] = DurationField

    if RelativeDeltaField is not None:
        mapping[RelativeDeltaField] = DurationField
