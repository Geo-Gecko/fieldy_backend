from rest_framework import serializers

from .models import WeeklyFieldIndicators


class WeeklyFieldIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeeklyFieldIndicators

        fields = '__all__'


class GetWeeklyFieldIndicatorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeeklyFieldIndicators
        ref_name = None

        fields = (
            'field_id','date_observed', 'field_ndvi', 'field_ndwi',
            'field_precipitation', 'field_temperature', 'field_evapotranspiration'
        )
