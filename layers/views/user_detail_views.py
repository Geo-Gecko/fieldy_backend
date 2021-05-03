import os

from django.shortcuts import get_object_or_404
from rest_framework import (
    exceptions,
    generics,
    status,
    serializers,
    viewsets
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from layers.models import ShUserDetail
from layers.views.polygon_views import verify_auth_token
from layers.serializers import ShUserDetailSerializer


class RetrieveCreateUpdateUserDetail(
    generics.CreateAPIView,
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
):

    serializer_class = ShUserDetailSerializer
    permission_classes = (AllowAny,)
    schema = None

    def create(self, request, uu_id):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        serializer_data['properties']['user_id'] = user["uid"]
        serializer = self.serializer_class(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, uu_id):
        user_data, user = verify_auth_token(request)
        if user_data != {}:
            return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user_obj = ShUserDetail.objects.get(user_id=user["uid"])
            serializer = self.serializer_class(user_obj)
            return Response(
                {"current_center": serializer.data, "user_detail": user},
                status=status.HTTP_200_OK
            )
        except ShUserDetail.DoesNotExist:
            return Response(
                {"current_center": None, "user_detail": user},
                status=status.HTTP_200_OK
            )


    def put(self, request, uu_id):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer_data['properties']['user_id'] = user["uid"]
        try:
            user_obj = ShUserDetail.objects.get(user_id=user["uid"])
            serializer = self.serializer_class(user_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ShUserDetail.DoesNotExist:
            serializer_data['properties']['user_id'] = user["uid"]
            serializer = self.serializer_class(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
