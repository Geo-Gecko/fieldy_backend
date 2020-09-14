import uuid

from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField

class PolygonLayer(models.Model):
    field_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    field_attributes = HStoreField(blank=True, default=dict)

    # GeoDjango-specific: a geometry field (PolygonField)
    shpolygon = models.PolygonField(blank=True)

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

class PointLayer(models.Model):
    field_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    field_attributes = HStoreField(blank=True, default=dict)
    shpoint = models.PointField(blank=True)

    def __str__(self):
        return self.name
