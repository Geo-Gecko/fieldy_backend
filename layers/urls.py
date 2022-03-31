from django.urls import include, path
from rest_framework.routers import DefaultRouter
from layers.views.contact_views import contact_us
from layers.views.polygon_views import (
    ListCreatePolygonLayer, get_fields_in_grid_cell,
    ListCreateUpdateDestroyGridLayer, get_fields, get_croptypes
)
from layers.views.indicator_views import (
    FieldIndicatorsViewSet, FieldIndicatorCalculationsViewSet,
    GetForeCastIndicatorsViewSet, AFSISIndicatorsViewSet,
    get_fieldindicators_for_fields_in_grid_cell
)
from layers.views.polygon_views import RetrieveUpdateDestroyPolygonLayer
from layers.views.user_detail_views import RetrieveCreateUpdateUserDetail
from layers.views.one_acre_views import get_last_visit_summaries

router = DefaultRouter()
router.register(
    "afsis-data", AFSISIndicatorsViewSet, basename="afsis-data"
)
router.register(
    "field-indicators", FieldIndicatorsViewSet, basename="field-indicators"
)
router.register(
    "indicator-calculations", FieldIndicatorCalculationsViewSet, basename="indicator-calculations"
)
router.register(
    "grid-layers", ListCreateUpdateDestroyGridLayer, basename="grid-layers"
)
router.register(
    "forecast-indicators", GetForeCastIndicatorsViewSet, basename="forecast-indicators"
)

app_name = 'layers'

urlpatterns = [
    # path('contact/', contact_us),
    path('fields/', get_fields),
    path('croptypes/', get_croptypes),
    path('fields/<str:field_id>/', get_fields),
    path('field-in-grid-cell/<str:grid_id>/', get_fields_in_grid_cell),
    path('kators-in-grid-cell/<str:grid_id>/', get_fieldindicators_for_fields_in_grid_cell),

    # one-acre-fund urls
    path('last-visit-summary/<int:month_>/', get_last_visit_summaries),

    path('listcreatepolygonlayer/', ListCreatePolygonLayer.as_view()),
    path(
        'getupdatedeletelayer/<str:field_id>/',
        RetrieveUpdateDestroyPolygonLayer.as_view()
    ),
    path(
        'getcreateupdateuserdetail/<str:uu_id>/',
        RetrieveCreateUpdateUserDetail.as_view()
    ),
    path('', include(router.urls))
]
