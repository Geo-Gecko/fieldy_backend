
from .models import ArrayedFieldIndicators


def delete_after_polygon(sender, instance, **kwargs):
    try:
        ArrayedFieldIndicators.objects.filter(field_id=instance.field_id).delete()
    except ArrayedFieldIndicators.DoesNotExist:
        pass
