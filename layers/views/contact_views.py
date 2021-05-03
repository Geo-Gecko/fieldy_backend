import os
import threading
from threading import Thread
from django.utils import timezone

from mailjet_rest import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from layers.views.polygon_views import verify_auth_token

class EmailThread(threading.Thread):
    def __init__(self, *message):
        self.user_id = message[0]
        self.message = message[1]
        threading.Thread.__init__(self)

    def run (self):
        api_key = os.environ.get('MAILJET_API_KEY', '')
        api_secret = os.environ.get('MAILJET_API_SECRET', '')
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
            {
            "From": {
                "Email": "baron@geogecko.com",
                "Name": "Stephen"
            },
            "To": [
                {
                "Email": "baron@geogecko.com",
                "Name": "Stephen"
                },
                {
                "Email": "info@geogecko.com",
                "Name": "GeoGecko Team"
                }
            ],
            "Subject": "Small Holder User",
            "TextPart": f"User with id {self.user_id}",
            "HTMLPart": f"Hello,<br/><br/> User with id {self.user_id} Left this message:<br/><br/> {self.message}",
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        result = mailjet.send.create(data=data)
        return result.json()


@api_view(['POST'])
def contact_us(request):
    user_data, user = verify_auth_token(request)
    if not user_data:
        return Response({"Error": "Unauthorized request"}, status=status.HTTP_403_FORBIDDEN)
    if not user_data.get('message'):
        return Response({"Error": "Message has been sent"}, status=status.HTTP_400_BAD_REQUEST)
    EmailThread(user["uid"], user_data.get('message')).start()
    return Response({"Messsage": "Email sent"}, status=status.HTTP_200_OK)
