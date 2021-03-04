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
from drf_yasg.utils import swagger_auto_schema
from layers.views.polygon_views import verify_auth_token

from layers.models import FieldIndicatorCalculations, ArrayedFieldIndicators
from layers.serializers import (
    FieldIndicatorsSerializer, FieldIndicatorCalculationsSerializer,
    GetFieldIndicatorCalculationsSerializer
)


class FieldIndicatorsViewSet(viewsets.ViewSet):

    serializer_class = FieldIndicatorsSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)

    def list(self, request):
        """
        To list all the indicators for all fields
        ---
        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 200
              message: OK

        produces:
            - application/json
        """
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user_member != "":
            user_id = user_member

        queryset = ArrayedFieldIndicators.objects.filter(user_id=user_id)
        serializer = self.serializer_class(queryset, many=True)
        # import json;
        # with open('moringa_2019_2020.json', 'w') as fa_:
        #     json.dump(serializer.data, fa_)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
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
        """
        To list all the indicators for a particular field
        ---
        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 200
              message: OK

        produces:
            - application/json
        """
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user_member != "":
            user_id = user_member

        field_ndvi_obj = ArrayedFieldIndicators.objects.filter(
            user_id=user_id, field_id=field_id
        )
        serializer = self.serializer_class(field_ndvi_obj, many=True)

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
            field_ndvi_obj = ArrayedFieldIndicators.objects.get(
                user_id=user_id, field_id=field_id
            )
            serializer = self.serializer_class(field_ndvi_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ArrayedFieldIndicators.DoesNotExist:
            serializer_data['user_id'] = user_id
            serializer = self.serializer_class(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldIndicatorCalculationsViewSet(viewsets.ViewSet):

    serializer_class = FieldIndicatorCalculationsSerializer
    lookup_field = 'indicator'
    permission_classes = (AllowAny,)
    schema = None

    def list(self, request):
        user_data, user_id, user_member = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user_member != "":
            user_id = user_member

        queryset = FieldIndicatorCalculations.objects.filter(user_id=user_id)
        serializer = GetFieldIndicatorCalculationsSerializer(
            queryset, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    # CREATE AND PUT TO BE EXCLUDED FROM DEPLOYED APP AS WELL
    # def create(self, request, indicator=None):
    #     serializer_data, user_id, user_member = verify_auth_token(request)
    #     if not serializer_data or user_member != "":
    #         return Response(
    #             {"Error": "Unauthorized request"},
    #             status=status.HTTP_403_FORBIDDEN
    #         )

    #     serializer_data['user_id'] = user_id
    #     serializer = self.serializer_class(data=serializer_data)

    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def put(self, request, indicator=None):
    #     serializer_data, user_id, user_member = verify_auth_token(request)
    #     if not serializer_data or user_member != "":
    #         return Response(
    #             {"Error": "Unauthorized request"},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     # check this line in the previous view
    #     serializer_data['user_id'] = user_id
    #     try:
    #         field_ndvi_obj = FieldIndicatorCalculations.objects.get(
    #             user_id=user_id, indicator=indicator
    #         )
    #         serializer = self.serializer_class(field_ndvi_obj, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #     except FieldIndicatorCalculations.DoesNotExist:
    #         serializer_data['user_id'] = user_id
    #         serializer = self.serializer_class(data=serializer_data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)
