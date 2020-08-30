from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import PointLayer, PolygonLayer

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
