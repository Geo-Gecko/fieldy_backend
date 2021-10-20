import os

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets, pagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import jwt

from layers.models import PolygonJsonLayer, GridJsonLayer
from layers.serializers import (
    PolygonLayerSerializer, GridLayerSerializer, GetGridLayerSerializer
)

def verify_auth_token(request):
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]
        try:
            user_ = jwt.decode(token, os.environ.get("SECRET_KEY", ""), algorithms="HS256")
            try:
                return request.data, user_
            except KeyError:
                return request.data, user_['uid']
        except jwt.exceptions.InvalidSignatureError:
            return False, ""
        except jwt.exceptions.DecodeError:
            return False, ""
    return False, ""



class PolygonResultsSetPagination(pagination.LimitOffsetPagination):
    default_limit = 2000
    max_limit = 2000


class ListCreatePolygonLayer(generics.ListCreateAPIView):
    """URL to list view and create polygons"""

    serializer_class = PolygonLayerSerializer
    permission_classes = (AllowAny,)
    pagination_class = PolygonResultsSetPagination
    schema = None

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        user_data, user = verify_auth_token(request)
        if user_data != {}:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        queryset = PolygonJsonLayer.objects.filter(user_id=user["uid"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.serializer_class(queryset, many=True)
        def move_field_user_ids(polygon_):
            for col_ in ["field_id", "user_id"]:
                polygon_["properties"][col_] = polygon_[col_]
                del polygon_[col_]
        list(map(move_field_user_ids, serializer.data))

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        serializer_data['properties']['user_id'] = user["uid"]
        for col_ in ["field_id", "user_id"]:
            serializer_data[col_] = serializer_data['properties'][col_]
            del serializer_data["properties"][col_]
        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"layer": serializer.data}, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyPolygonLayer(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = PolygonJsonLayer.objects.all()
    serializer_class = PolygonLayerSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'field_id'
    schema = None

    def put(self, request, field_id):
        serializer_data, user = verify_auth_token(request)
        # TODO: ADD AUTHORIZATION...
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        layer_ = get_object_or_404(
            PolygonJsonLayer, field_id=field_id, user_id=user["uid"]
        )
        serializer = self.serializer_class(layer_, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, field_id):
        user_data, user = verify_auth_token(request)
        if user_data != {} or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        layer_ = get_object_or_404(
            PolygonJsonLayer, field_id=field_id, user_id=user["uid"]
        )
        layer_.delete()

        return Response(
            {"message": "Layer has been deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class ListCreateUpdateDestroyGridLayer(viewsets.ModelViewSet):
    """URL to list view and create Gridpolygons"""

    serializer_class = GridLayerSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)
    queryset = GridJsonLayer.objects.all()
    schema = None

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        user_data, user = verify_auth_token(request)
        if user_data != {}:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        queryset = GridJsonLayer.objects.filter(user_id=user["uid"])
        serializer = GetGridLayerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: do not push create or put methods
    # def create(self, request):
    #     serializer_data, user = verify_auth_token(request)
    #     if not serializer_data or user["memberOf"] != "":
    #         return Response(
    #             {"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN
    #         )

    #     serializer_data['properties']['user_id'] = user["uid"]
    #     serializer = self.serializer_class(data=serializer_data)

    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response({"layer": serializer.data}, status=status.HTTP_201_CREATED)

    # def put(self, request, field_id=None):
    #     serializer_data, user = verify_auth_token(request)
    #     if not serializer_data or user["memberOf"] != "":
    #         return Response(
    #             {"Error": "Unauthorized request"},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     # check this line in the previous view
    #     serializer_data['user_id'] = user["uid"]
    #     try:
    #         field_ndvi_obj = GridJsonLayer.objects.get(
    #             user_id=user["uid"], field_id=field_id
    #         )
    #         serializer = self.serializer_class(field_ndvi_obj, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #     except GridJsonLayer.DoesNotExist:
    #         serializer_data['user_id'] = user["uid"]
    #         serializer = self.serializer_class(data=serializer_data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request, field_id):
    #     user_data, user = verify_auth_token(request)
    #     if user_data != {} or user["memberOf"] != "":
    #         return Response(
    #             {"Error": "Unauthorized request"},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     layer_ = get_object_or_404(
    #         GridJsonLayer, field_id=field_id, user_id=user["uid"]
    #     )
    #     layer_.delete()

        # return Response(
        #     {"message": "Layer has been deleted"},
        #     status=status.HTTP_204_NO_CONTENT
        # )
