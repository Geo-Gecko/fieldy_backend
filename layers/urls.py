from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from layers.views.contact_views import contact_us
from layers.views.polygon_views import ListCreatePolygonLayer
from layers.views.indicator_views import FieldIndicatorsViewSet
from layers.views.polygon_views import RetrieveUpdateDestroyPolygonLayer
from layers.views.user_detail_views import RetrieveCreateUpdateUserDetail

router = DefaultRouter()
router.register('fieldindicators', FieldIndicatorsViewSet, basename="fieldindicators")

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
