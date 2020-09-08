import os

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
import jwt

from .models import PolygonLayer, PointLayer
from .serializers import PointLayerSerializer, PolygonLayerSerializer

def verify_auth_token(request):
    token = request.headers["Authorization"]
    token = token.split(" ")[1]
    if token:
        try:
            user_ = jwt.decode(token, os.environ.get("SECRET_KEY", ""), algorithms="HS256")
            return request.data
        except jwt.exceptions.InvalidSignatureError:
            return False
    return False


class ListCreateLayers(generics.ListCreateAPIView):
    """Class for creation of an article"""

    queryset = None
    serializer_class = None
    permission_classes = (AllowAny,)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        user_data = verify_auth_token(request)
        if user_data != {}:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer_data = verify_auth_token(request)
        if not serializer_data:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"layer": serializer.data}, status=status.HTTP_201_CREATED)

class ListCreatePointLayer(ListCreateLayers):

    serializer_class = PointLayerSerializer
    queryset = PointLayer.objects.all()


class ListCreatePolygonLayer(ListCreateLayers):

    serializer_class = PolygonLayerSerializer
    queryset = PolygonLayer.objects.all()
