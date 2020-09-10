import uuid

from django.contrib.gis.db import models

class PolygonLayer(models.Model):
    field_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )

    # GeoDjango-specific: a geometry field (PolygonField)
    shpolygon = models.PolygonField(blank=True)

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

class PointLayer(models.Model):
    field_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    shpoint = models.PointField(blank=True)

    def __str__(self):
        return self.name
