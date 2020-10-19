from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from layers.views import (
    ListCreatePolygonLayer, RetrieveUpdateDestroyPolygonLayer,
    RetrieveCreateUpdateUserDetail, FieldIndicatorsViewSet
)

router = DefaultRouter()
router.register('fieldindicators', FieldIndicatorsViewSet, basename="fieldindicators")

urlpatterns = [
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
