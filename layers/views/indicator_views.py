import os
from datetime import datetime, timedelta

from rest_framework import (
    status,
    viewsets,
    pagination,
    mixins
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from layers.views.polygon_views import verify_auth_token
from layers.models import (
    FieldIndicatorCalculations, ArrayedFieldIndicators,
    ForeCastIndicators, AFSISIndicators, PolygonJsonLayer
)
from layers.serializers import (
    FieldIndicatorsSerializer, FieldIndicatorCalculationsSerializer,
    GetFieldIndicatorCalculationsSerializer, GetForeCastIndicatorsSerializer,
    GetFieldIndicatorsSerializer, ForeCastIndicatorsSerializer,
    AFSISIndicatorsSerializer, GetAFSISIndicatorsSerializer,
)


class IndicatorResultsSetPagination(pagination.LimitOffsetPagination):
    default_limit = 50000
    max_limit = 50000



@api_view(['GET'])
def get_fieldindicators_for_fields_in_grid_cell(request, grid_id):
    """Return all indicators fields in a grid cell

    Args:
        request (GET): All indicators for fields in a grid cell

    Returns:
        [200]: List of indicators for fields in grid cell
    """
    user_data, user = verify_auth_token(request)
    if user_data != {}:
        return Response(
            {"Error": "Unauthorized request"},
            status=status.HTTP_403_FORBIDDEN
        )
    if user["memberOf"] != "":
        user["uid"] = user["memberOf"]

    try:
        fields_queryset = PolygonJsonLayer.objects.filter(properties__gridId=grid_id)
        try:
            queryset = ArrayedFieldIndicators.objects.filter(
                field_id__in=(row.field_id for row in fields_queryset)
            )
            serializer = GetFieldIndicatorsSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArrayedFieldIndicators.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except PolygonJsonLayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class AFSISIndicatorsViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin
):

    serializer_class = AFSISIndicatorsSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)
    pagination_class = IndicatorResultsSetPagination

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: GetAFSISIndicatorsSerializer(many=True)}
    )
    def list(self, request):
        """
        List AFSIS for fields
        ---
        produces:
            - application/json
        """
        user_data, user = verify_auth_token(request)
        if user_data != {} or user["paymentLevels"] != "SECOND LEVEL":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        queryset = AFSISIndicators.objects.filter(user_id=user["uid"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetAFSISIndicatorsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GetAFSISIndicatorsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer_data['user_id'] = user["uid"]
        serializer = self.serializer_class(data=serializer_data)

        # NOTE: Comment this out on deploying
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, field_id=None):
        """
        List AFSIS for a particular field
        ---
        responseMessages:
            - code: 401
              message: Not authenticated
            - code: 200
              message: OK

        produces:
            - application/json
        """
        user_data, user = verify_auth_token(request)
        if user_data != {} or user["paymentLevels"] != "SECOND LEVEL":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        field_afsis_obj = AFSISIndicators.objects.filter(
            user_id=user["uid"], field_id=field_id
        )
        serializer = GetAFSISIndicatorsSerializer(field_afsis_obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        # check this line in the previous view
        serializer_data['user_id'] = user["uid"]
        try:
            field_ndvi_obj = AFSISIndicators.objects.get(
                user_id=user["uid"], field_id=field_id
            )
            serializer = self.serializer_class(field_ndvi_obj, data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
        except AFSISIndicators.DoesNotExist:
            serializer_data['user_id'] = user["uid"]
            serializer = self.serializer_class(data=serializer_data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldIndicatorsViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin
):

    serializer_class = FieldIndicatorsSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)
    pagination_class = IndicatorResultsSetPagination

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: GetFieldIndicatorsSerializer(many=True)}
    )
    def list(self, request):
        """
        To list all the indicators for all fields
        ---
        produces:
            - application/json
        """
        user_data, user = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        queryset = ArrayedFieldIndicators.objects.filter(user_id=user["uid"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetFieldIndicatorsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GetFieldIndicatorsSerializer(queryset, many=True)
        # import json;
        # with open('moringa_2019_2020.json', 'w') as fa_:
        #     json.dump(serializer.data, fa_)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer_data['user_id'] = user["uid"]
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
        user_data, user = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        field_ndvi_obj = ArrayedFieldIndicators.objects.filter(
            user_id=user["uid"], field_id=field_id
        )
        serializer = GetFieldIndicatorsSerializer(field_ndvi_obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        # check this line in the previous view
        serializer_data['user_id'] = user["uid"]
        try:
            field_ndvi_obj = ArrayedFieldIndicators.objects.get(
                user_id=user["uid"], field_id=field_id
            )
            serializer = self.serializer_class(field_ndvi_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ArrayedFieldIndicators.DoesNotExist:
            serializer_data['user_id'] = user["uid"]
            serializer = self.serializer_class(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

# NOTE: viewsets.ViewSet doesn't have put or delete
class FieldIndicatorCalculationsViewSet(viewsets.ModelViewSet):

    serializer_class = FieldIndicatorCalculationsSerializer
    lookup_field = 'indicator'
    permission_classes = (AllowAny,)
    schema = None

    def list(self, request):
        user_data, user = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        queryset = FieldIndicatorCalculations.objects.filter(user_id=user["uid"])
        serializer = GetFieldIndicatorCalculationsSerializer(
            queryset, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: CREATE AND PUT TO BE EXCLUDED FROM DEPLOYED APP AS WELL
    def create(self, request, indicator=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer_data['user_id'] = user["uid"]
        serializer = self.serializer_class(data=serializer_data)

        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, indicator=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        # check this line in the previous view
        serializer_data['user_id'] = user["uid"]
        try:
            field_ndvi_obj = FieldIndicatorCalculations.objects.get(
                user_id=user["uid"], indicator=indicator, crop_type=request.data["crop_type"]
            )
            serializer = self.serializer_class(field_ndvi_obj, data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
        except FieldIndicatorCalculations.DoesNotExist:
            serializer_data['user_id'] = user["uid"]
            serializer = self.serializer_class(data=serializer_data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



class GetForeCastIndicatorsViewSet(viewsets.ViewSet):

    serializer_class = ForeCastIndicatorsSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)
    schema = None

    def list(self, request):
        user_data, user = verify_auth_token(request)
        if user_data != {}:
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        queryset = ForeCastIndicators.objects.filter(user_id=user["uid"])
        serializer = GetForeCastIndicatorsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: CREATE AND PUT TO BE EXCLUDED FROM DEPLOYED APP
    def create(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer_data['user_id'] = user["uid"]
        serializer = self.serializer_class(data=serializer_data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        # check this line in the previous view
        serializer_data['user_id'] = user["uid"]
        try:
            forecast_obj = ForeCastIndicators.objects.get(
                user_id=user["uid"], field_id=field_id
            )
            serializer = self.serializer_class(forecast_obj, data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
        except ForeCastIndicators.DoesNotExist:
            serializer_data['user_id'] = user["uid"]
            serializer = self.serializer_class(data=serializer_data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

