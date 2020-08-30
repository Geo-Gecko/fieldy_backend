from django.contrib.gis.db import models

class PolygonLayer(models.Model):
    #name = models.CharField(max_length=50)

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    shpolygon = models.MultiPolygonField(blank=True)

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

class PointLayer(models.Model):
    #name = models.CharField(max_length=50)
    shpoint = models.PointField(blank=True)

    def __str__(self):
        return self.name
