import os

from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportQueryError

# Select your transport with a defined url endpoint
transport = RequestsHTTPTransport(
    url=os.environ.get('LOGIN_SERVER', 'http://localhost:4000/graphql')
)

# Create a GraphQL client using the defined transport
client = Client(transport=transport)

@api_view(['POST'])
def get_auth_token(request):
    """
    To get a token for authenticated use of field indicatos
    ---
    parameters_strategy: merge
    parameters:
        - name: username
          required: true
          type: string
          paramType: form
        - name: password
          required: true
          type: string
          paramType: form
    responseMessages:
        - code: 401
            message: Not authenticated
        - code: 201
            message: Created

    produces:
        - application/json
        - application/xml
    """

    query = gql(
        """
    mutation Login($username: String!, $password: String!) {
        login(username: $username, password: $password) {
        token
        }
    }
    """
    )
    params = request.data.keys()

    if len(params) > 2:
        return Response(
            {"Messsage": "Only username and password are required"}, status=status.HTTP_400_BAD_REQUEST
        )
    elif "username" not in params or "password" not in params:
        return Response(
            {"Messsage": "username or password are missing"}, status=status.HTTP_400_BAD_REQUEST
        )
    else:
        try:
            result = client.execute(query, variable_values=request.data)
            return Response(result, status=status.HTTP_200_OK)
        except TransportQueryError as error:
            return Response(
                {"Messsage": error.__dict__['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
            import pdb; pdb.set_trace()
