import os

from django.shortcuts import get_object_or_404
from rest_framework import (
    exceptions,
    generics,
    status,
    serializers,
    viewsets
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
import jwt

from .models import PolygonLayer, PointLayer, ShUserDetail, FieldIndicators
from .serializers import (
    PointLayerSerializer, PolygonLayerSerializer,
    ShUserDetailSerializer, FieldIndicatorsSerializer
)

def verify_auth_token(request):
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        try:
            user_ = jwt.decode(token, os.environ.get("SECRET_KEY", ""), algorithms="HS256")
            try:
                return request.data, user_['uid'], user_['memberOf']
            except KeyError:
                return request.data, user_['uid']
        except jwt.exceptions.InvalidSignatureError:
            return False, "", ""
        except jwt.exceptions.DecodeError:
            return False, "", ""
    return False, "", ""


class ListCreatePolygonLayer(generics.ListCreateAPIView):
    """Class for creation of an article"""

    serializer_class = PolygonLayerSerializer
    permission_classes = (AllowAny,)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {}:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        if user_member != "":
            user_id = user_member

        queryset = PolygonLayer.objects.filter(user_id=user_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer_data, user_id, user_member = verify_auth_token(request)
        if not serializer_data or user_member != "":
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        serializer_data['properties']['user_id'] = user_id
        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"layer": serializer.data}, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyPolygonLayer(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = PolygonLayer.objects.all()
    serializer_class = PolygonLayerSerializer
    permission_classes = (AllowAny,)

    def put(self, request, field_id):
        serializer_data, user_id, user_member = verify_auth_token(request)
        if not serializer_data:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        layer_ = get_object_or_404(
            PolygonLayer, field_id=field_id, user_id=user_id
        )
        serializer = self.serializer_class(layer_, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, field_id):
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {} or user_member != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        layer_ = get_object_or_404(
            PolygonLayer, field_id=field_id, user_id=user_id
        )
        layer_.delete()

        return Response(
            {"message": "Layer has been deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

class RetrieveCreateUpdateUserDetail(
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
):

    serializer_class = ShUserDetailSerializer
    permission_classes = (AllowAny,)

    def create(self, request, uu_id):
        serializer_data, user_id, user_member = verify_auth_token(request)
        if not serializer_data:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        serializer_data['properties']['user_id'] = user_id
        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, uu_id):
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {}:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        user_obj = get_object_or_404(ShUserDetail, user_id=user_id)
        serializer = self.serializer_class(user_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uu_id):
        serializer_data, user_id, user_member = verify_auth_token(request)
        if not serializer_data:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer_data['properties']['user_id'] = user_id
        try:
            user_obj = ShUserDetail.objects.get(user_id=user_id)
            serializer = self.serializer_class(user_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ShUserDetail.DoesNotExist:
            serializer_data['properties']['user_id'] = user_id
            serializer = self.serializer_class(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class FieldIndicatorsViewSet(viewsets.ViewSet):

    serializer_class = FieldIndicatorsSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)

    def list(self, request):
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user_member != "":
            user_id = user_member

        queryset = FieldIndicators.objects.filter(user_id=user_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, field_id=None):
        serializer_data, user_id, user_member = verify_auth_token(request)
        if not serializer_data or user_member != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer_data['user_id'] = user_id
        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, field_id=None):
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user_member != "":
            user_id = user_member

        field_ndvi_obj = get_object_or_404(
            FieldIndicators, user_id=user_id, field_id=field_id, year=2019
        )
        serializer = self.serializer_class(field_ndvi_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, field_id=None):
        serializer_data, user_id, user_member = verify_auth_token(request)
        if not serializer_data or user_member != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        # check this line in the previous view
        serializer_data['user_id'] = user_id
        try:
            field_ndvi_obj = FieldIndicators.objects.get(
                user_id=user_id, field_id=field_id
            )
            serializer = self.serializer_class(field_ndvi_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except FieldIndicators.DoesNotExist:
            serializer_data['user_id'] = user_id
            serializer = self.serializer_class(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
