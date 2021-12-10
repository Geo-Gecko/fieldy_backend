
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from indicator_analytics.views import FieldIndicatorsTopBottomViewSet

router = DefaultRouter()

router.register(
    "fieldindicatorstopbottom", FieldIndicatorsTopBottomViewSet, basename="fieldindicatorstopbottom"
)

app_name = 'indicator_analytics'

urlpatterns = [path('', include(router.urls))]