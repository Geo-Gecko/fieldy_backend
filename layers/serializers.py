from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import PointLayer, PolygonLayer, ShUserDetail, FieldIndicators

class PolygonLayerSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PolygonLayer
        geo_field = "shpolygon"

        fields = '__all__'


class PointLayerSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PointLayer
        geo_field = "shpoint"

        fields = '__all__'

class ShUserDetailSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ShUserDetail
        geo_field = "center"

        fields = '__all__'


class FieldIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldIndicators

        fields = '__all__'
