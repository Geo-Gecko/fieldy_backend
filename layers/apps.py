from django.apps import AppConfig
from django.db.models.signals import post_delete


class LayersConfig(AppConfig):
    name = 'layers'

    def ready(self):
        from .models import PolygonLayer
        from .signals import delete_after_polygon
        post_delete.connect(delete_after_polygon, sender=PolygonLayer)
