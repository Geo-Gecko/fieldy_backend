from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import (
    PointLayer, PolygonLayer, ShUserDetail, ForeCastIndicators,
    ArrayedFieldIndicators, GridLayer, FieldIndicatorCalculations
)

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

class GridLayerSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GridLayer
        geo_field = "shpolygon"

        fields = '__all__'


class GetGridLayerSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GridLayer
        geo_field = "shpolygon"

        fields = ("field_id", "count", "field_attributes", "shpolygon")


class ShUserDetailSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = ShUserDetail
        geo_field = "center"

        fields = '__all__'


class FieldIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArrayedFieldIndicators

        fields = '__all__'

class GetFieldIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArrayedFieldIndicators

        fields = (
            'field_id','indicator', 'january', 'february', 'march', 'april', 'may',
            'june', 'july', 'august', 'september', 'october', 'november', 'december' 
        )

class FieldIndicatorCalculationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldIndicatorCalculations

        fields = '__all__'

class GetFieldIndicatorCalculationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldIndicatorCalculations

        exclude = ('user_id', 'id', )


class ForeCastIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForeCastIndicators

        fields = '__all__'

class GetForeCastIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForeCastIndicators

        fields = (
            'field_id','avg_temperature', 'sum_precipitation', 'day'
        )
