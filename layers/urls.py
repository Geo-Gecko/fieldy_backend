from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from layers.views.contact_views import contact_us
from layers.views.polygon_views import (
    ListCreatePolygonLayer, ListCreateUpdateDestroyGridLayer
)
from layers.views.indicator_views import (
    FieldIndicatorsViewSet, FieldIndicatorCalculationsViewSet,
    GetForeCastIndicatorsViewSet, FieldIndicatorsTopBottomViewSet, AFSISIndicatorsViewSet
)
from layers.views.polygon_views import RetrieveUpdateDestroyPolygonLayer
from layers.views.user_detail_views import RetrieveCreateUpdateUserDetail

router = DefaultRouter()
router.register(
    "afsisdata", AFSISIndicatorsViewSet, basename="afsisdata"
)
router.register(
    "fieldindicators", FieldIndicatorsViewSet, basename="fieldindicators"
)
router.register(
    "fieldindicatorstopbottom", FieldIndicatorsTopBottomViewSet, basename="fieldindicatorstopbottom"
)
router.register(
    "indicatorcalculations", FieldIndicatorCalculationsViewSet, basename="indicatorcalculations"
)
router.register(
    "gridlayers", ListCreateUpdateDestroyGridLayer, basename="gridlayers"
)
router.register(
    "forecastindicators", GetForeCastIndicatorsViewSet, basename="forecastindicators"
)

app_name = 'layers'

urlpatterns = [
    # path('contact/', contact_us),
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
