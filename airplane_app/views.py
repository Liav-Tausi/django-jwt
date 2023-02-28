from django.contrib import auth
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from airplane_app.serializers import *


# Create your views here.


class FlightModelViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = {
        "list": BaseAllSerializer,
        "retrieve": BaseAllSerializer,
        "create": CreateFlightSerializer,
        "update": BaseAllSerializer,
        "partial_update": BaseAllSerializer,
        "destroy": DestroyFlightSerializer,
    }

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializer_class[self.action]


class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = {
        "list": BaseOrderSerializer,
        "retrieve": BaseOrderSerializer,
        "create": BaseOrderSerializer,
        "update": BaseOrderSerializer,
        "partial_update": BaseOrderSerializer,
        "destroy": DestroyFlightSerializer,
    }

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializer_class[self.action]


class UserModelViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = BaseUserSerializer
