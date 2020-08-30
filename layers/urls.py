from django.urls import include, path
from rest_framework import routers
from layers.views import CreatePointLayer, CreatePolygonLayer

urlpatterns = [
    path('createpointlayer/', CreatePointLayer.as_view()),
    path('createpolygonlayer/', CreatePolygonLayer.as_view()),
]


# urlpatterns = format_suffix_patterns(urlpatterns)