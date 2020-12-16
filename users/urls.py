from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import get_auth_token


urlpatterns = [
    path('authtoken/', get_auth_token)
]
