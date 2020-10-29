import uuid

from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.validators import KeysValidator

MONTHS_ = (
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
)


class PolygonLayer(models.Model):
    field_id = models.UUIDField(
        editable=True, unique=True
    )
    field_attributes = HStoreField(blank=True, default=dict)
    user_id = models.CharField(max_length=30, blank=False)

    # GeoDjango-specific: a geometry field (PolygonField)
    shpolygon = models.PolygonField(blank=True)

    # Returns the string representation of the model.
    def __str__(self):
        return str(self.field_id)

class PointLayer(models.Model):
    field_id = models.UUIDField(
        editable=True, unique=True
    )
    field_attributes = HStoreField(blank=True, default=dict)
    user_id = models.CharField(max_length=30, blank=False)
    shpoint = models.PointField(blank=True)

    def __str__(self):
        return str(self.field_id)

class ShUserDetail(models.Model):
    user_id = models.CharField(max_length=30, blank=False)
    center = models.PointField(blank=True)
    zoom_level = models.IntegerField(blank=True)

    def __str__(self):
        return self.user_id

class FieldIndicators(models.Model):
    field_id = models.UUIDField(
        editable=True, unique=False
    )
    user_id = models.CharField(max_length=30, blank=False)
    year = models.IntegerField(blank=True)
    field_ndvi = HStoreField(
        validators=[KeysValidator(keys=MONTHS_, strict=True)],
        default=dict
    )
    # these values are collected for a whole area are they not???
    field_ndwi = HStoreField(
        validators=[KeysValidator(keys=MONTHS_, strict=True)],
        default=dict
    )
    field_rainfall = HStoreField(
        validators=[KeysValidator(keys=MONTHS_, strict=True)],
        default=dict
    )
    field_temperature = HStoreField(
        validators=[KeysValidator(keys=MONTHS_, strict=True)],
        default=dict
    )

    def __str__(self):
        return str(self.field_id)
