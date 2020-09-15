from django.urls import include, path
from rest_framework import routers
from layers.views import (
    ListCreatePolygonLayer, RetrieveUpdateDestroyPolygonLayer,
    RetrieveCreateUpdateUserDetail
)

urlpatterns = [
    path('listcreatepolygonlayer/', ListCreatePolygonLayer.as_view()),
    path(
        'getupdatedeletelayer/<str:field_id>/',
        RetrieveUpdateDestroyPolygonLayer.as_view()
    ),
    path(
        'getcreateupdateuserdetail/<str:uu_id>/',
        RetrieveCreateUpdateUserDetail.as_view()
    )
]
