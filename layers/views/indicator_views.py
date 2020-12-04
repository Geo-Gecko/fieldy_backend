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
from layers.views.polygon_views import verify_auth_token

from layers.models import FieldIndicators
from layers.serializers import FieldIndicatorsSerializer


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
        # import json;
        # with open('moringa_2019_2020.json', 'w') as fa_:
        #     json.dump(serializer.data, fa_)
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
            FieldIndicators, user_id=user_id, field_id=field_id
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
