from datetime import datetime

from django.utils import timezone
from django.test import TestCase
from django.db.utils import IntegrityError

from layers.models import (
    PolygonJsonLayer, GridJsonLayer, FieldIndicatorCalculations,
    ShUserDetail, ArrayedFieldIndicators, ForeCastIndicators, AFSISIndicators
)


class PolygonModelTest(TestCase):

    def setUp(self):
        self.type="Feature"
        self.user_id="5f9fe31fefe94f000b4bg22c"
        self.field_id="2f51437b-b9b4-5a15-abcd-5f8f457d80c0"

    def test_polygon_creation(self):
        self.old_count = PolygonJsonLayer.objects.count()
        PolygonJsonLayer.objects.create(
            type=self.type, field_id=self.field_id,
            user_id=self.user_id, properties={"type": "json_field"},
            geometry={"type": "Polygon", "coordinates": [[
                [45.758967495894076, -10.557028521799048], [45.75897161370394, -10.556967340730041],
                [45.75903250410639, -10.556971478163786], [39.75902838629586, -3.557032659304134],
                [39.758967495894076, -3.557028521799048]
            ]]}
        )
        self.new_count = PolygonJsonLayer.objects.count()
        self.assertNotEqual(self.old_count, self.new_count)

    def test_grid_creation(self):
        self.old_count = GridJsonLayer.objects.count()
        GridJsonLayer.objects.create(
            type=self.type, field_id=self.field_id,
            user_id=self.user_id, properties={"type": "json_field"},
            geometry={"type": "Polygon", "coordinates": [[
                [45.758967495894076, -10.557028521799048], [45.75897161370394, -10.556967340730041],
                [45.75903250410639, -10.556971478163786], [39.75902838629586, -3.557032659304134],
                [39.758967495894076, -3.557028521799048]
            ]]}
        )
        self.new_count = GridJsonLayer.objects.count()
        self.assertNotEqual(self.old_count, self.new_count)

    def test_user_creation(self):
        self.old_count = ShUserDetail.objects.count()
        ShUserDetail.objects.create(
            type=self.type, user_id=self.user_id, zoom_level=10,
            geometry={"type": "Point", "coordinates": [-14.309630880716188, 33.63464355468751]}
        )
        self.new_count = ShUserDetail.objects.count()
        self.assertNotEqual(self.old_count, self.new_count)

    def test_fieldindicators_creation(self):
        self.old_count = ArrayedFieldIndicators.objects.count()
        ArrayedFieldIndicators.objects.create(
            field_id=self.field_id, user_id=self.user_id, indicator="field_ndvi",
            january=0.11, february =0.13, march = 0.16, april = 0.11, may=0.11,
            june = 0.17, july = 0.15, august = 0.13, september = 0.12, october = 0.13,
            november = 0.19, december = 0.15
        )
        self.new_count = ArrayedFieldIndicators.objects.count()
        self.assertNotEqual(self.old_count, self.new_count)

    def test_non_duplication_of_indicator_data(self):
        ArrayedFieldIndicators.objects.create(
            field_id=self.field_id, user_id=self.user_id, indicator="field_ndvi",
            january=0.11, february =0.13, march = 0.16, april = 0.11, may=0.11,
            june = 0.17, july = 0.15, august = 0.13, september = 0.12, october = 0.13,
            november = 0.19, december = 0.15
        )
        with self.assertRaises(IntegrityError):
            ArrayedFieldIndicators.objects.create(
                field_id=self.field_id, user_id=self.user_id, indicator="field_ndvi",
                january=0.11, february =0.13, march = 0.16, april = 0.11, may=0.11,
                june = 0.17, july = 0.15, august = 0.13, september = 0.12, october = 0.13,
                november = 0.19, december = 0.15
            )

    def test_fieldindicatorcalculations_creation(self):
        self.old_count = FieldIndicatorCalculations.objects.count()
        FieldIndicatorCalculations.objects.create(
            user_id=self.user_id, indicator="field_ndvi", crop_type="Maize",
            january=0.11, february =0.13, march = 0.16, april = 0.11, may=0.11,
            june = 0.17, july = 0.15, august = 0.13, september = 0.12, october = 0.13,
            november = 0.19, december = 0.15
        )
        self.new_count = FieldIndicatorCalculations.objects.count()
        self.assertNotEqual(self.old_count, self.new_count)

    def test_non_duplication_of_indicator_calculations_data(self):
        FieldIndicatorCalculations.objects.create(
            user_id=self.user_id, indicator="field_ndvi", crop_type="Maize",
            january=0.11, february =0.13, march = 0.16, april = 0.11, may=0.11,
            june = 0.17, july = 0.15, august = 0.13, september = 0.12, october = 0.13,
            november = 0.19, december = 0.15
        )
        with self.assertRaises(IntegrityError):
            FieldIndicatorCalculations.objects.create(
                user_id=self.user_id, indicator="field_ndvi", crop_type="Maize",
                january=0.11, february =0.13, march = 0.16, april = 0.11, may=0.11,
                june = 0.17, july = 0.15, august = 0.13, september = 0.12, october = 0.13,
                november = 0.19, december = 0.15
            )

    def test_forecastindicators_creation(self):
        self.old_count = ForeCastIndicators.objects.count()
        ForeCastIndicators.objects.create(
            field_id=self.field_id, day=timezone.now(), user_id=self.user_id,
            avg_temperature=25, sum_precipitation=0.5
        )
        self.new_count = ForeCastIndicators.objects.count()
        self.assertNotEqual(self.old_count, self.new_count)


    def test_non_duplication_of_forecastindicators_calculation(self):
        day_ = timezone.now()
        ForeCastIndicators.objects.create(
            field_id=self.field_id, day=day_, user_id=self.user_id,
            avg_temperature=25, sum_precipitation=0.5
        )
        with self.assertRaises(IntegrityError):
            ForeCastIndicators.objects.create(
                field_id=self.field_id, day=day_, user_id=self.user_id,
                avg_temperature=25, sum_precipitation=0.5
            )

    def test_afsisindicators_creation(self):
        self.old_count = AFSISIndicators.objects.count()
        AFSISIndicators.objects.create(
            field_id=self.field_id, user_id=self.user_id, field_aluminium=50,
            field_bedrock=200, field_carbon=18, field_fcc=3512, field_ph=59
        )
        self.new_count = AFSISIndicators.objects.count()
        self.assertNotEqual(self.old_count, self.new_count)

    def test_non_duplication_of_afsisindicators_creation(self):
        AFSISIndicators.objects.create(
            field_id=self.field_id, user_id=self.user_id, field_aluminium=50,
            field_bedrock=200, field_carbon=18, field_fcc=3512, field_ph=59
        )
        with self.assertRaises(IntegrityError):
            AFSISIndicators.objects.create(
                field_id=self.field_id, user_id=self.user_id, field_aluminium=50,
                field_bedrock=200, field_carbon=18, field_fcc=3512, field_ph=59
            )
"""
5cf7c51d-6388-4b98-b47b-327547959782 | 615b402fe822c8000aa5b3bf | field_ndvi | 0.1125806018 | 0.132732365 | 0.111091499 | 0.1522725089 | 0.1987788166 | 0.1257804658 | 0.2357646751 | 0.206517935 | 0.1977465567 | 0.313875118 |     0.26 |    0.198
"""