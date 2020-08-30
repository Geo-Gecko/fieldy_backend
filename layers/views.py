from django.shortcuts import render
from rest_framework import (
    exceptions,
    generics,
    status,
    serializers
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response

from .serializers import PointLayerSerializer, PolygonLayerSerializer

class CreateLayer(generics.CreateAPIView):
    """Class for creation of an article"""

    serializer_class = None
    permission_classes = (AllowAny,)
    # authentication_classes = (JWTAuthentication,)

    def create(self, request):
        serializer_data = request.data
        print(serializer_data)

        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"layer": serializer.data}, status=status.HTTP_201_CREATED)

class CreatePointLayer(CreateLayer):

    serializer_class = PointLayerSerializer


class CreatePolygonLayer(CreateLayer):

    serializer_class = PolygonLayerSerializer
