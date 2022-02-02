
from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from indicator_analytics.views import (
    FieldIndicatorsTopBottomViewSet, FieldIndicatorsNDVIChangeViewSet,
    WeeklyFieldIndicatorsViewSet, FieldIndicatorsThresholdsViewSet, monthly_delete
)

router = DefaultRouter()

router.register(
    "field-indicators-top-bottom", FieldIndicatorsTopBottomViewSet, basename="field-indicators-top-bottom"
)
router.register(
    "ndvi-change", FieldIndicatorsNDVIChangeViewSet, basename="ndvi-change"
)
router.register(
    'weekly-indicators', WeeklyFieldIndicatorsViewSet, basename='weekly-indicators'
)
router.register(
    'field-indicator-thresholds', FieldIndicatorsThresholdsViewSet, basename='field-indicator-thresholds'
)

app_name = 'indicator_analytics'

urlpatterns = [
    path('', include(router.urls)),
    url(r'^monthly-delete/$', monthly_delete, name = "monthly-delete")
]
