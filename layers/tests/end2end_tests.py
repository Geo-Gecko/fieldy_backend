import os

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[11.488282, 8.79171], [11.4878, 8.7918], [11.4877, 8.7917],
                        [11.4877, 8.7916], [11.4878, 8.7916], [11.488282, 8.79171]]
                    ]
                    },
                "properties": {
                    "field_id": "bde0c225-d488-4abb-b039-768579078720",
                    "field_attributes": {"Area": "0", "CropType": "15"},
                    "user_id": "5f34961f33d7d212dc71322c"
                }
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {os.environ.get('TEST_TOKEN', '')}"
        )


    def test_can_create_layer(self):
        response = self.client.post('/layers/listcreatepolygonlayer/', self.feature,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_not_create_layer_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        response = self.client.post('/layers/listcreatepolygonlayer/', self.feature,
                                    format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
