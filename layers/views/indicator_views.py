import os
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from rest_framework import (
    status,
    viewsets,
    pagination,
    mixins
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from layers.views.polygon_views import verify_auth_token
from layers.models import (
    FieldIndicatorCalculations, ArrayedFieldIndicators,
    ForeCastIndicators, AFSISIndicators
)
from layers.serializers import (
    FieldIndicatorsSerializer, FieldIndicatorCalculationsSerializer,
    GetFieldIndicatorCalculationsSerializer, GetForeCastIndicatorsSerializer,
    GetFieldIndicatorsSerializer, ForeCastIndicatorsSerializer,
    AFSISIndicatorsSerializer, GetAFSISIndicatorsSerializer,
)


from rest_framework import pagination


MONTHS_ = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]
available_indicators = [
            "field_rainfall", "field_ndvi", "field_ndwi",
            "field_temperature", "field_evapotranspiration"
        ]

class IndicatorResultsSetPagination(pagination.LimitOffsetPagination):
    default_limit = 50000
    max_limit = 50000



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
        if user_data != {} or user["memberOf"] != "61164207eaef91000adcfeab":
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
        if user_data != {}:
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



class FieldIndicatorsTopBottomViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin
):

    serializer_class = FieldIndicatorsSerializer
    lookup_field = 'indicator'
    permission_classes = (AllowAny,)
    pagination_class = IndicatorResultsSetPagination

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'indicator', openapi.IN_QUERY,
            description="indicator type to retrieve", type=openapi.TYPE_STRING, default="field_rainfall"
        ),
        openapi.Parameter(
            'month', openapi.IN_QUERY, description="month for retrieval", type=openapi.TYPE_STRING, default="previous month"
        ),
        openapi.Parameter(
            'position', openapi.IN_QUERY, description="top or bottom results to retrieve", type=openapi.TYPE_STRING, default="top"
        ),
        openapi.Parameter(
            'percentage', openapi.IN_QUERY, description="number of results to obtain as a percentage of total results per indicator per month",
            type=openapi.TYPE_INTEGER, default=15
        )
    ],
    responses={status.HTTP_200_OK: GetFieldIndicatorsSerializer(many=True)},
    )
    def list(self, request):
        """
        Query analytics
        """
        user_data, user = verify_auth_token(request)
        if user_data != {} or user["memberOf"] != "61164207eaef91000adcfeab":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        previous_month = datetime.now() - timedelta(days=30)
        previous_month = previous_month.strftime("%B").lower()
        indicator = request.query_params.get("indicator", "field_rainfall")
        month_ = request.query_params.get("month", previous_month)
        position = request.query_params.get("position", "top")
        percentage = request.query_params.get("percentage", 15)

        if month_ not in MONTHS_:
             return Response(
                {"Error": "Month provided should be of lower case, like: january"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if position not in ["top", "bottom"]:
             return Response(
                {"Error": "Position should be either top or bottom"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if indicator not in available_indicators:
             return Response(
                {"Error": f"Available indicators are: {available_indicators}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if int(percentage) < 0 or int(percentage) > 100:
                return Response(
                    {"Error": "Optimal percentage range should be between 1 and 50"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError as e:
             return Response(
                {"Error": "Optimal percentage range should be between 1 and 50"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = ArrayedFieldIndicators.objects.filter(
            user_id=user["uid"], indicator=indicator
        ).order_by(f"-{month_}")

        if position == "top":
            queryset = queryset[:round(len(queryset) * int(percentage)/100)]
        elif position == "bottom":
            queryset = queryset[len(queryset) - round(len(queryset) * int(percentage)/100):]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetFieldIndicatorsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GetFieldIndicatorsSerializer(queryset, many=True)

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

