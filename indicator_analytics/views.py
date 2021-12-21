
from itertools import groupby, chain
from datetime import datetime, timedelta

from drf_yasg import openapi
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework import (
    status,
    viewsets,
    mixins
)

from layers.serializers import (
    FieldIndicatorsSerializer,
    GetFieldIndicatorsSerializer
)
from layers.models import ArrayedFieldIndicators
from layers.views.polygon_views import verify_auth_token
from layers.views.indicator_views import IndicatorResultsSetPagination

from .models import WeeklyFieldIndicators
from .serializers import (
    WeeklyFieldIndicatorsSerializer, GetWeeklyFieldIndicatorsSerializer
)

MONTHS_ = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]
available_indicators = [
            "field_rainfall", "field_ndvi", "field_ndwi",
            "field_temperature", "field_evapotranspiration"
        ]


class WeeklyFieldIndicatorsViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin
):

    serializer_class = WeeklyFieldIndicatorsSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)
    pagination_class = IndicatorResultsSetPagination


    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'earliest_month', openapi.IN_QUERY, default="previous month",
            description="furthest month back to be retrieved", type=openapi.TYPE_STRING,
        )
    ],
    responses={status.HTTP_200_OK: GetWeeklyFieldIndicatorsSerializer(many=True)},
    )
    def list(self, request):
        """
        To list all the weekly indicators for all the fields
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

        earliest_month = datetime.now() - timedelta(days=42)
        earliest_month = earliest_month.strftime("%B").lower()
        earliest_month = request.query_params.get("earliest_month", earliest_month)
        if earliest_month not in MONTHS_:
            return Response(
                {"Error": f"Month passed should be among: {MONTHS_}"},
                status=status.HTTP_403_FORBIDDEN
            )
        if type(earliest_month) == str:
            # TODO: This line below is iffy. now is november...earliest is feb...calculate
            year = datetime.now().year if MONTHS_.index(earliest_month)+1 - datetime.now().month < 0 else (datetime.now() - timedelta(days=366)).year
            earliest_month = datetime.strptime(f"{earliest_month.capitalize()}/{year}", "%B/%Y")

        queryset = WeeklyFieldIndicators.objects.filter(
            user_id=user["uid"], date_observed__gt=earliest_month
        ).order_by("-date_observed")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetWeeklyFieldIndicatorsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GetWeeklyFieldIndicatorsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "" or user["paymentLevels"] != "SECOND LEVEL":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer_data['user_id'] = user["uid"]
        serializer = self.serializer_class(data=serializer_data)

        # serializer.is_valid(raise_exception=True)
        # serializer.save()

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
        if user_data != {} or user["paymentLevels"] != "SECOND LEVEL":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "" or user["paymentLevels"] != "SECOND LEVEL":
            user["uid"] = user["memberOf"]

        earliest_month = datetime.now() - timedelta(days=42)
        earliest_month = earliest_month.strftime("%B").lower()
        earliest_month = request.query_params.get("earliest_month", earliest_month)
        if earliest_month not in MONTHS_:
            return Response(
                {"Error": f"Month passed should be among: {MONTHS_}"},
                status=status.HTTP_403_FORBIDDEN
            )
        if type(earliest_month) == str:
            year = datetime.now().year if MONTHS_.index(earliest_month)+1 - datetime.now().month < 0 else (datetime.now() - timedelta(days=366)).year
            earliest_month = datetime.strptime(f"{earliest_month.capitalize()}/{year}", "%B/%Y")#.strftime("%Y-%m-%d")

        field_ndvi_obj = WeeklyFieldIndicators.objects.filter(
            user_id=user["uid"], date_observed__gt=earliest_month, field_id=field_id
        ).order_by("-date_observed")

        serializer = GetWeeklyFieldIndicatorsSerializer(field_ndvi_obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, field_id=None):
        serializer_data, user = verify_auth_token(request)
        if not serializer_data or user["memberOf"] != "" or user["paymentLevels"] != "SECOND LEVEL":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )
        # check this line in the previous view
        serializer_data['user_id'] = user["uid"]
        try:
            field_ndvi_obj = WeeklyFieldIndicators.objects.get(
                user_id=user["uid"], field_id=field_id
            )
            serializer = self.serializer_class(field_ndvi_obj, data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
        except WeeklyFieldIndicators.DoesNotExist:
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
        Query Top and bottom performing fields
        """
        user_data, user = verify_auth_token(request)
        if user_data != {} or user["paymentLevels"] != "SECOND LEVEL":
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


class FieldIndicatorsNDVIChangeViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin
):

    serializer_class = WeeklyFieldIndicatorsSerializer
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)
    pagination_class = IndicatorResultsSetPagination

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'earliest_month', openapi.IN_QUERY, default="previous month",
            description="furthest month back to be retrieved", type=openapi.TYPE_STRING,
        )
    ],
        responses={status.HTTP_200_OK: GetWeeklyFieldIndicatorsSerializer(many=True)},
    )
    def list(self, request):
        """
        Query NDVI Changes
        """
        user_data, user = verify_auth_token(request)
        if user_data != {} or user["paymentLevels"] != "SECOND LEVEL":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        earliest_month = datetime.now() - timedelta(days=42)
        earliest_month = earliest_month.strftime("%B").lower()
        earliest_month = request.query_params.get("earliest_month", earliest_month)
        if earliest_month not in MONTHS_:
            return Response(
                {"Error": f"Month passed should be among: {MONTHS_}"},
                status=status.HTTP_403_FORBIDDEN
            )
        if type(earliest_month) == str:
            year = datetime.now().year if MONTHS_.index(earliest_month)+1 - datetime.now().month < 0 else (datetime.now() - timedelta(days=366)).year
            earliest_month = datetime.strptime(f"{earliest_month.capitalize()}/{year}", "%B/%Y")#.strftime("%Y-%m-%d")

        queryset = WeeklyFieldIndicators.objects.filter(
            user_id=user["uid"], date_observed__gt=earliest_month
        ).order_by("-date_observed")

        def get_differences(results_):
            group_fids = []
            list_results = list(results_.data)
            # groupby needs the sorting
            list_results.sort(key=lambda x: x["field_id"])
            for k,g in groupby(list_results, key=lambda x: x["field_id"]):
                group_fids.append(list(g))
            for field_data in group_fids:
                for i, row_ in enumerate(field_data):
                    try:
                        row_[f"{row_['date_observed']} - {field_data[i+1]['date_observed']}"] = row_["field_ndvi"] - field_data[i+1]["field_ndvi"]
                        for kator in available_indicators:
                            try:
                                del row_[kator]
                            except KeyError:
                                del row_["field_precipitation"]
                        del row_['date_observed']
                    except IndexError:
                        continue
                # exclude last element in the group since it wasn't subtracted from anything
            results_ = list(chain.from_iterable([el[:len(el) - 1] for el in group_fids]))
            return results_

        page = self.paginate_queryset(queryset)
        if page is not None:
            results_ = GetWeeklyFieldIndicatorsSerializer(page, many=True)
            results_ = get_differences(results_)
            return self.get_paginated_response(results_)
        else:
            results_ = GetWeeklyFieldIndicatorsSerializer(queryset, many=True)
            results_ = get_differences(results_)
        
        return Response(results_, status=status.HTTP_200_OK)
