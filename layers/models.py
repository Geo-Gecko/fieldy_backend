import uuid

from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField

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
        return self.field_id

class PointLayer(models.Model):
    field_id = models.UUIDField(
        editable=True, unique=True
    )
    field_attributes = HStoreField(blank=True, default=dict)
    user_id = models.CharField(max_length=30, blank=False)
    shpoint = models.PointField(blank=True)

    def __str__(self):
        return self.field_id

class ShUserDetail(models.Model):
    user_id = models.CharField(max_length=30, blank=False)
    center = models.PointField(blank=True)
    zoom_level = models.IntegerField(blank=True)

    def __str__(self):
        return self.user_id
