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

from .serializers import PointLayerSerializer, PolygonLayerSerializer

def verify_auth_token(request):
    # import pdb; pdb.set_trace()
    token = request.headers["Authorization"]
    token = token.split(" ")[1]
    if token:
        try:
            user_ = jwt.decode(token, os.environ.get("SECRET_KEY", ""), algorithms="HS256")
            return request.data
        except jwt.exceptions.InvalidSignatureError:
            return False
    return False


class CreateLayer(generics.CreateAPIView):
    """Class for creation of an article"""

    serializer_class = None
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer_data = verify_auth_token(request)
        if not serializer_data:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"layer": serializer.data}, status=status.HTTP_201_CREATED)

class CreatePointLayer(CreateLayer):

    serializer_class = PointLayerSerializer


class CreatePolygonLayer(CreateLayer):

    serializer_class = PolygonLayerSerializer
