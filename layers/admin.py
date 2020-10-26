from django.contrib import admin
from layers.models import (
    PolygonLayer, PointLayer, ShUserDetail, FieldIndicators
)

# Register your models here.
admin.site.register(PolygonLayer)
admin.site.register(PointLayer)
admin.site.register(ShUserDetail)
admin.site.register(FieldIndicators)