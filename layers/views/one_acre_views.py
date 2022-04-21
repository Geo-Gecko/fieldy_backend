import os
from datetime import datetime

from django.db.models import Count
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from layers.models import PolygonJsonLayer
from layers.views.polygon_views import verify_auth_token


@api_view(['GET'])
def get_last_visit_summaries(request, month_=1):
    """Return last visits less or equal to a month

    Returns:
        [200]: List date-visited-field-count dictionaries
    """
    user_data, user = verify_auth_token(request)
    if user_data != {}:
        return Response(
            {"Error": "Unauthorized request"},
            status=status.HTTP_403_FORBIDDEN
        )

    if user["memberOf"] != "":
        user["uid"] = user["memberOf"]
    
    if user["uid"] != "623731215344c1000aae2459":
        return Response(
            {"Error": "This data is not available for this account"},
            status=status.HTTP_403_FORBIDDEN
        )
    if month_ > 12:
        return Response(
            {"Error": "Max and min available months are 0 and 12"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        results_ = PolygonJsonLayer.objects.filter(user_id=user["uid"]).annotate(
            LastVisit=KeyTextTransform("LastVisit", "properties")
        ).values("LastVisit").annotate(fieldCount=Count("LastVisit"))
        results_ = list(filter(
            lambda row_: (
                datetime.now() - datetime.strptime(row_["LastVisit"], '%Y-%m-%d')
            ).days // 31 <= month_, results_
        ))
        results_.sort(key=lambda row_: row_["LastVisit"])
        return Response(results_, status=status.HTTP_200_OK)
    except PolygonJsonLayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_status_summaries(request, status_="Currently"):
    """Return ownership status of one acre fund fields

    Returns:
        [200]: Dictionary of counts per status
    """
    user_data, user = verify_auth_token(request)
    if user_data != {}:
        return Response(
            {"Error": "Unauthorized request"},
            status=status.HTTP_403_FORBIDDEN
        )

    if user["memberOf"] != "":
        user["uid"] = user["memberOf"]
    
    if user["uid"] != "623731215344c1000aae2459":
        return Response(
            {"Error": "This data is not available for this account"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        results_ = PolygonJsonLayer.objects.filter(user_id=user["uid"]).annotate(
            OAFStatus=KeyTextTransform("OAFStatus", "properties")
        ).values("OAFStatus").annotate(fieldCount=Count("OAFStatus"))
        results__ = PolygonJsonLayer.objects.filter(user_id=user["uid"]).values("properties")
        results___ = list(filter(lambda row_: (row_["properties"]["OAFStatus"] == status_), results__))
        reduced = []
        for row_ in results___:
            reduced.append(row_["properties"]["gridId"])
        res = {}
        for i in reduced:
            res[i] = reduced.count(i)
        
        return Response([results_, res], status=status.HTTP_200_OK)
    except PolygonJsonLayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
