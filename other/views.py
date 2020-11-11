from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from .models import AgeGroup, AdministrativeDivision, AttendanceType, GradeTypeGroup
from .serializers import AgeGroupSerializer, AttendanceTypeSerializer, AdministrativeDivisionSerializer, \
    GradeTypeGroupWithTypesSerializer, FilterDataSerializer

import constants


class FilterDataViewSet(GenericViewSet,
                        ListModelMixin):
    queryset = AgeGroup.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return FilterDataSerializer
        return FilterDataSerializer

    def list(self, request, *args, **kwargs):
        ages = AgeGroup.objects.all()
        age_serializer = AgeGroupSerializer(ages, many=True)
        attendance_types = AttendanceType.objects.all()
        attendance_serializer = AttendanceTypeSerializer(attendance_types, many=True)
        grade_groups = GradeTypeGroup.objects.all()
        grade_serializer = GradeTypeGroupWithTypesSerializer(grade_groups, many=True)
        administrative_divisions = AdministrativeDivision.objects.all()
        administrative_divisions_serializer = AdministrativeDivisionSerializer(administrative_divisions, many=True)
        data = {
            'age_groups': age_serializer.data,
            'attendance_types': attendance_serializer.data,
            'administrative_divisions': administrative_divisions_serializer.data,
            'grade_groups': grade_serializer.data,
            'time_types': constants.TIMES
        }
        return Response(data)

