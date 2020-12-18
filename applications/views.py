from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from .models import BookingApplication
from .serializers import BookingApplicationCreateSerializer, PartnershipApplicationCreateSerializer


class BookingApplicationViewSet(GenericViewSet,
                                CreateModelMixin):
    queryset = BookingApplication.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingApplicationCreateSerializer
        return BookingApplicationCreateSerializer


class PartnershipApplicationViewSet(GenericViewSet,
                                    CreateModelMixin):
    queryset = BookingApplication.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'create':
            return PartnershipApplicationCreateSerializer
        return PartnershipApplicationCreateSerializer


