
from .models import ArrayedFieldIndicators, FieldIndicators


def delete_after_polygon(sender, instance, **kwargs):
    try:
        FieldIndicators.objects.get(field_id=instance.field_id).delete()
        ArrayedFieldIndicators.objects.filter(field_id=instance.field_id).delete()
    except FieldIndicators.DoesNotExist:
        pass
    except ArrayedFieldIndicators.DoesNotExist:
        pass
