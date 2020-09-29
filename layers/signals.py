
from .models import PolygonLayer, FieldNdvi


def delete_after_polygon(sender, instance, **kwargs):
    try:
        FieldNdvi.objects.get(field_id=instance.field_id).delete()
    except FieldNdvi.DoesNotExist:
        pass
