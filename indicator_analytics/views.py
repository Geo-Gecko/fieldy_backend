
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


MONTHS_ = [
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december'
]
available_indicators = [
            "field_rainfall", "field_ndvi", "field_ndwi",
            "field_temperature", "field_evapotranspiration"
        ]

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

    serializer_class = FieldIndicatorsSerializer
    lookup_field = 'indicator'
    permission_classes = (AllowAny,)
    pagination_class = IndicatorResultsSetPagination

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: GetFieldIndicatorsSerializer(many=True)},
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

        def get_differences(results_):
            for row_ in results_.data:
                for i, month_ in enumerate(MONTHS_):
                    try:
                        row_[f"{month_}_{MONTHS_[i+1]}_difference"] = round(row_[month_] - row_[MONTHS_[i+1]], 2)
                        del row_[month_]
                    except IndexError:
                        row_[f"{month_}_difference"] = "Waiting for coming month"
                        del row_[month_]
                        continue
                    except TypeError:
                        row_[f"{month_}_difference"] = "Next month had no value"
                        del row_[month_]
            return results_

        queryset = ArrayedFieldIndicators.objects.filter(
            user_id=user["uid"], indicator="field_ndvi"
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            results_ = GetFieldIndicatorsSerializer(page, many=True)
            results_ = get_differences(results_)
            return self.get_paginated_response(results_.data)
        else:
            results_ = GetFieldIndicatorsSerializer(queryset, many=True)
            results_ = get_differences(results_)
        
        return Response(results_.data, status=status.HTTP_200_OK)
