from django.db.models.manager import Manager
from django.db.utils import Error
from indicator_analytics.managers import SoftDeleteManager
from django.db import models


class WeeklyFieldIndicators(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["field_id", "date_observed"],
                name="unique weekly field indicators row"
            )
        ]

    field_id = models.UUIDField(
        editable=True, unique=False
    )
    user_id = models.CharField(max_length=30, blank=False)
    date_observed = models.DateField(blank=False)
    field_ndvi = models.FloatField(blank=True, null=True)
    field_ndwi = models.FloatField(blank=True, null=True)
    field_precipitation = models.FloatField(blank=True, null=True)
    field_temperature = models.FloatField(blank=True, null=True)
    field_evapotranspiration = models.FloatField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager() # https://www.youtube.com/watch?v=nlZHpGPkfbQ
    all_objects = Manager()

    def restore(self):
        self.deleted = False
        self.save()

    def soft_delete(self):
        self.deleted = True
        self.save()

    def delete(self):
        raise Error()
