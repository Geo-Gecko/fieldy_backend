import uuid

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.validators import KeysValidator

MONTHS_ = (
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
)


class PolygonJsonLayer(models.Model):
    type = models.CharField(max_length=15, blank=False)
    field_id = models.UUIDField(
        editable=True, unique=True
    )
    user_id = models.CharField(max_length=30, blank=False)
    properties = models.JSONField(blank=True, default=dict)

    # GeoDjango-specific: a geometry field (PolygonField)
    geometry = models.JSONField(blank=True, default=dict)

    # Returns the string representation of the model.
    def __str__(self):
        return str(self.field_id)


class PolygonLayer(gis_models.Model):
    field_id = models.UUIDField(
        editable=True, unique=True
    )
    field_attributes = HStoreField(blank=True, default=dict)
    user_id = models.CharField(max_length=30, blank=False)

    # GeoDjango-specific: a geometry field (PolygonField)
    shpolygon = gis_models.PolygonField(blank=True)

    # Returns the string representation of the model.
    def __str__(self):
        return str(self.field_id)



class GridJsonLayer(models.Model):
    type = models.CharField(max_length=15, blank=False)
    field_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    # field_id is to be used to update the fields
    user_id = models.CharField(max_length=30, blank=False)
    properties = models.JSONField(blank=True, default=dict)
    geometry = models.JSONField(blank=True, unique=True)

    def __str__(self):
        return str(self.field_id)


class GridLayer(gis_models.Model):
    # TODO: this should be layer_id
    field_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # field_id is to be used to update the fields
    user_id = models.CharField(max_length=30, blank=False)
    count = models.FloatField(null=True)
    field_attributes = HStoreField(blank=True, default=dict)
    shpolygon = gis_models.PolygonField(blank=True, unique=True)

    def __str__(self):
        return str(self.field_id)


class ShUserDetail(models.Model):
    type = models.CharField(max_length=15, blank=False, default="Feature")
    user_id = models.CharField(max_length=30, blank=False)
    geometry = models.JSONField(blank=True, default=dict)
    zoom_level = models.IntegerField(blank=True)

    def __str__(self):
        return self.user_id


class ArrayedFieldIndicators(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["field_id", "indicator"],
                name="unique field indicators row"
            )
        ]

    field_id = models.UUIDField(
        editable=True, unique=False
    )
    user_id = models.CharField(max_length=30, blank=False)
    indicator = models.CharField(max_length=50, blank=False)
    january = models.FloatField(null=True)
    february = models.FloatField(null=True)
    march = models.FloatField(null=True)
    april = models.FloatField(null=True)
    may = models.FloatField(null=True)
    june = models.FloatField(null=True)
    july = models.FloatField(null=True)
    august = models.FloatField(null=True)
    september = models.FloatField(null=True)
    october = models.FloatField(null=True)
    november = models.FloatField(null=True)
    december = models.FloatField(null=True)


class FieldIndicatorCalculations(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "indicator", "crop_type"],
                name="unique indicator row"
            )
        ]

    user_id = models.CharField(max_length=30, blank=False)
    crop_type = models.CharField(max_length=50, blank=False)
    indicator = models.CharField(max_length=50, blank=False)
    january = models.FloatField(null=True)
    february = models.FloatField(null=True)
    march = models.FloatField(null=True)
    april = models.FloatField(null=True)
    may = models.FloatField(null=True)
    june = models.FloatField(null=True)
    july = models.FloatField(null=True)
    august = models.FloatField(null=True)
    september = models.FloatField(null=True)
    october = models.FloatField(null=True)
    november = models.FloatField(null=True)
    december = models.FloatField(null=True)


class ForeCastIndicators(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["field_id", "day"],
                name="unique forecast row"
            )
        ]

    field_id = models.UUIDField(
        editable=True, unique=False
    )
    day = models.DateTimeField(blank=False)
    user_id = models.CharField(max_length=30, blank=False)
    avg_temperature = models.FloatField(null=True)
    sum_precipitation = models.FloatField(null=True)
