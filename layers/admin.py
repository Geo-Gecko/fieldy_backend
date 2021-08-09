from django.contrib import admin
from layers.models import (
    PolygonJsonLayer, ShUserDetail, ArrayedFieldIndicators
)

# Register your models here.
admin.site.register(PolygonJsonLayer)
admin.site.register(ShUserDetail)
admin.site.register(ArrayedFieldIndicators)
