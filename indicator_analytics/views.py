import os
import json
from copy import deepcopy
from calendar import monthrange
from itertools import groupby, chain
from datetime import datetime, timedelta, date

from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework import (
    status,
    viewsets,
    mixins
)
from rest_framework import serializers
from rest_framework.decorators import api_view
import requests


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
            "field_precipitation", "field_ndvi", "field_ndwi",
            "field_temperature", "field_evapotranspiration"
        ]


@swagger_auto_schema(method="delete", auto_schema=None)
@api_view(['DELETE'])
def monthly_delete(request):
    user_data, user = verify_auth_token(request)
    if user_data != {} or user["memberOf"] != "" or user["paymentLevels"] != "SECOND LEVEL":
        return Response(
            {"Error": "Unauthorized request"},
            status=status.HTTP_403_FORBIDDEN
        )
    old_date = datetime.now() - timedelta(days=365)
    old_data = WeeklyFieldIndicators.objects.filter(
        date_observed__lte=old_date
    ).order_by("date_observed")
    if len(old_data):
        for data_ in old_data:
            data_.soft_delete()

        deleted_date1, deleted_date2 = old_data[0].date_observed, old_data[len(old_data) - 1].date_observed
        deleted_date1, deleted_date2 = deleted_date1.strftime("%d-%m-%Y"), deleted_date2.strftime("%d-%m-%Y")
        return Response(
            {"message": f"Weekly data has been softly deleted. Dates captured are: {deleted_date1, deleted_date2}"},
            status=status.HTTP_204_NO_CONTENT
        )
    return Response({"message": "No existing data for deletion"}, status=status.HTTP_200_OK)

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
            user_id=user["uid"], date_observed__gte=earliest_month
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
            user_id=user["uid"], date_observed__gte=earliest_month, field_id=field_id
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
            'month', openapi.IN_QUERY, description="month up to which data is retrieved", type=openapi.TYPE_INTEGER, default="previous month"
        ),
        openapi.Parameter(
            'week', openapi.IN_QUERY, description="week in the month up to which data is retrieved",
            type=openapi.TYPE_STRING, default="last week of the previous month - 4"
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

        previous_month = datetime.now() - timedelta(days=31)
        previous_month = previous_month.strftime("%B").lower()
        indicator = request.query_params.get("indicator", "field_rainfall")
        month_ = request.query_params.get("month", previous_month)
        try:
            week_ = int(request.query_params.get("week", 4))
        except ValueError:
             return Response(
                {"Error": "Week value should be an integer from 1 to 4"},
                status=status.HTTP_400_BAD_REQUEST
            )
        position = request.query_params.get("position", "top")
        percentage = request.query_params.get("percentage", 15)

        if not isinstance(week_, int) or week_ > 4 or week_ < 0:
             return Response(
                {"Error": "Week value should be an integer from 1 to 4"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if month_ not in MONTHS_:
             return Response(
                {"Error": "Month provided should be of lower case, like: january"},
                status=status.HTTP_400_BAD_REQUEST
            )
        year_ = datetime.now().year if MONTHS_.index(month_)+1 - datetime.now().month < 0\
            else (datetime.now() - timedelta(days=366)).year
        
        month_ = MONTHS_.index(month_) + 1
        # monthrange is because some months are 30,31,28. 
        # Also, subtracting the previous 31 days is so we can add on the weeks specified
        date_ = date(
            year_, month_, monthrange(year_, month_)[1]
        ) - timedelta(days=31) + timedelta(weeks=week_)

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

        queryset = WeeklyFieldIndicators.objects.filter(
            user_id=user["uid"], date_observed__gte=date_
        ).order_by("date_observed", f"-{indicator}")

        group_qset = [list(v) for k,v in groupby(queryset, lambda row: row.date_observed)]

        if position == "top":
            group_qset = [grp[:round(len(grp) * int(percentage)/100)] for grp in group_qset]
            queryset = list(chain.from_iterable(group_qset))
        elif position == "bottom":
            group_qset = [grp[len(grp) - round(len(grp) * int(percentage)/100):] for grp in group_qset]
            queryset = list(chain.from_iterable(group_qset))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetWeeklyFieldIndicatorsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GetWeeklyFieldIndicatorsSerializer(queryset, many=True)

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
        Query weekly NDVI Changes
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
            user_id=user["uid"], date_observed__gte=earliest_month
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



class FieldIndicatorsThresholdsViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin
):

    serializer_class = WeeklyFieldIndicators
    lookup_field = 'field_id'
    permission_classes = (AllowAny,)
    pagination_class = IndicatorResultsSetPagination

    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'indicator', openapi.IN_QUERY,
            description="indicator type to retrieve", type=openapi.TYPE_STRING, default="field_ndvi"
        ),
        openapi.Parameter(
            'earliest_month', openapi.IN_QUERY, description="earliest month for retrieval", type=openapi.TYPE_STRING, default="previous month"
        ),
        openapi.Parameter(
            'below', openapi.IN_QUERY,
            description="Retrieve fields for which indicator is below this value",
            type=openapi.TYPE_NUMBER, default=json.dumps({
                "field_ndvi": 0.2, "field_precipitation": 3, "field_ndwi": 0, "field_temperature": 15
            })
        ),
        openapi.Parameter(
            'above', openapi.IN_QUERY,
            description="Retrieve fields for which indicator is above this value",
            type=openapi.TYPE_NUMBER, default=json.dumps({
                "field_ndvi": None, "field_precipitation": None, "field_ndwi": 0.3, "field_temperature": 35
            })
        ),
    ],
    responses={status.HTTP_200_OK: GetWeeklyFieldIndicatorsSerializer(many=True)},
    )
    def list(self, request):
        """
        Query weekly field indicators using thresholds
        """
        user_data, user = verify_auth_token(request)
        if user_data != {} or user["paymentLevels"] != "SECOND LEVEL":
            return Response(
                {"Error": "Unauthorized request"},
                status=status.HTTP_403_FORBIDDEN
            )

        if user["memberOf"] != "":
            user["uid"] = user["memberOf"]

        kator_thresholds = {
            "field_ndvi": [0.2, None], "field_precipitation": [3, None],
            "field_ndwi": [0, 0.3], "field_temperature": [15, 35]
        }

        indicator = request.query_params.get("indicator", "field_ndvi")
        below = request.query_params.get("below", kator_thresholds[indicator][0])
        above = request.query_params.get("above", kator_thresholds[indicator][1])

        precip_sub = deepcopy(available_indicators)
        precip_sub[0] = "field_precipitation"
        if indicator not in precip_sub:
             return Response(
                {"Error": f"Available indicators are: {precip_sub}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if (above and float(above) > 1000) or float(below) < -1000:
                return Response(
                    {"Error": f"Issue with below and above values: {below}, {above}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError as e:
             return Response(
                {"Error": "Below and above values should be integers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        earliest_month = datetime.now() - timedelta(days=42)
        earliest_month = earliest_month.strftime("%B").lower()
        earliest_month = request.query_params.get("earliest_month", earliest_month)
        if earliest_month not in MONTHS_:
            return Response(
                {"Error": f"Month passed should be among: {MONTHS_}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Add +1 because datetime.now().month count is from 1
        year = datetime.now().year if MONTHS_.index(earliest_month)+1 - datetime.now().month < 0 else (datetime.now() - timedelta(days=366)).year
        earliest_month = datetime.strptime(f"{earliest_month.capitalize()}/{year}", "%B/%Y")

        # https://stackoverflow.com/a/11442041 ** translates k:v to k=v
        query_dict_ = {f"{indicator}__lt": below}
        if above:
            query_dict_[f"{indicator}__gt"] = above
        queryset = WeeklyFieldIndicators.objects.filter(
            user_id=user["uid"], date_observed__gte=earliest_month, **query_dict_
        ).order_by(f"-date_observed")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetWeeklyFieldIndicatorsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = GetWeeklyFieldIndicatorsSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# TODO: aUto delete old_data



@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["slope", "elevation", "land cover", "fertility capability classification"],
        properties={
            'slope': openapi.Schema(
                description="[min max] values of slope filter",
                type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
            ),
            'elevation': openapi.Schema(
                description="[min, max] values for elevation filter",
                type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
            ),
            'land cover': openapi.Schema(
                description="[min, max] values for land cover filter",
                type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
            ),
            'fertility capability classification': openapi.Schema(
                description="[min, max] values for fertility capability classification filter",
                type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
            ),
        }
    ),
    responses={status.HTTP_200_OK: serializers.Serializer({"Bounds": {}, "Grid": {"FeatureCollection": "..."}})},
)
@api_view(['POST'])
def wider_area(request):
    """Get all or fitlered wider area.
    """
    serializer_data, user = verify_auth_token(request)
    if not serializer_data or user["paymentLevels"] != "SECOND LEVEL" or user["memberOf"] != "61164207eaef91000adcfeab":
        return Response(
            {"Error": "Unauthorized request"},
            status=status.HTTP_403_FORBIDDEN
        )

    # NOTE: To be used for storing creds, the memberOf id I mean
    if user["memberOf"] != "":
        user["uid"] = user["memberOf"]

    #TODO: to be generated from user_auth
    client_auth = (os.getenv("GEOSERVER_NAME", ""), os.getenv("GEOSERVER_PASSWORD", ""))

    headers = {'Content-Type': 'application/json'}
    #Data Link
    get_data_url = os.getenv("GEOSERVER_URL", "") #nigeria_HT_grid&outputFormat=application%2Fjson'


    #First Generate List of AOI.
    #For each area/maybe when selected set the client_aoi
    client_aoi = 'kenya_HT_grid'
    client_aoi_summary = 'kenya_Grid_Summary'

    #The thresholds would apply when the data has been filtered on the platform and then the download button clicked.
    #Or if not prefiltered the default is no filter applied bu tthe user may specify which values they want to remove anyways via modal.

    #filterRequestCapability add '&cql_filter=slope%3E40'

    summary_request_url = f"{get_data_url}{client_aoi_summary}&outputFormat=application%2Fjson"
    summary_r = requests.get(summary_request_url, headers=headers, auth=client_auth)
    if summary_r.status_code == 200:
        summary_r = summary_r.json()
        summary_r = summary_r["features"][0]['properties']
    else:
        return Response({"Error": "Issue with third-party server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # fcc = fertility capability classification | lc - land cover
    filters_ = ['slope', 'elevation', 'land cover', 'fertility capability classification']

    if request.data.keys():
        param_filters = request.data.keys()
        for key_ in param_filters:
            if key_ not in filters_:
                return Response(
                    {"Error": f"Available filters are {filters_}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        param_values = chain.from_iterable(request.data.values())
        if not all(isinstance(val_, int) for val_ in param_values):
            return Response(
                {"Error": f"Ensure values are used for all filters"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not all(val_ <= 9700 or val_ > 0 for val_ in param_values):
            return Response(
                {"Error": "Maximum available value is 9700 for fertility-capability-classification. Min value is 0 for all"},
                status=status.HTTP_400_BAD_REQUEST
            )

        filter_query = '&cql_filter='
        for key_, val_ in request.data.items():
            if key_ == "land cover" or key_ == "fertility capability classification":
                key_ = "".join([x[0] for x in key_.split(" ")])
            query_ = f"{key_} between {val_[0]} and {val_[1]} and "
            filter_query += query_
        # remove last " and "
        filter_query = filter_query[:-5]

        filtered_request_url = f"{get_data_url}{client_aoi}{filter_query}&outputFormat=application%2Fjson"

        filtered_r = requests.get(filtered_request_url, headers=headers, auth=client_auth)
        if filtered_r.status_code == 200:
            filtered_data = filtered_r.json()
            return Response(
                {"Bounds": summary_r, "Grid": filtered_data}, status=status.HTTP_200_OK
            )
        return Response({"Error": "Issue with third-party server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Can be heavy result, but can load a tiff of the file, rather than the geojson, much lighter. slightly interactible.
    response = requests.get(f'{get_data_url}{client_aoi}&outputFormat=application%2Fjson', headers = headers, auth=client_auth)
    if response.status_code == 200:
        wider_area_data = response.json()
        return Response({"Bounds": summary_r, "Grid": wider_area_data}, status=status.HTTP_200_OK)
    return Response({"Error": "Issue with third-party server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
