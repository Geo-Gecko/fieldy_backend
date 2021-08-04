from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import (
    PolygonLayer, PolygonJsonLayer, ShUserDetail, ForeCastIndicators,
    ArrayedFieldIndicators, GridLayer, FieldIndicatorCalculations
)

class PolygonLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolygonJsonLayer

        fields = ("type", "field_id", "user_id", "properties", "geometry")


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


class ShUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShUserDetail

        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["properties"] = {}
        for col_ in ["user_id", "zoom_level"]:
            representation["properties"][col_] = representation[col_]
            del representation[col_]

        return representation

    def to_internal_value(self, data):
        for col_ in ["user_id", "zoom_level"]:
            data[col_] = data["properties"][col_]
        del data["properties"]


        return super().to_internal_value(data)

class FieldIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArrayedFieldIndicators

        fields = '__all__'

class GetFieldIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArrayedFieldIndicators
        ref_name = None

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
