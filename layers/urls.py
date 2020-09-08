from django.urls import include, path
from rest_framework import routers
from layers.views import (
    ListCreatePointLayer, ListCreatePolygonLayer
)

urlpatterns = [
    path('listcreatepointlayer/', ListCreatePointLayer.as_view()),
    path('listcreatepolygonlayer/', ListCreatePolygonLayer.as_view()),
]


# urlpatterns = format_suffix_patterns(urlpatterns)