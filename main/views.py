from django.db.models import Q

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .models import Course
from .serializers import CourseListSerializer
from .filters import CoursesMobileFilterBackend
from other.models import AgeGroup
from utils import pagination, test_data

import constants, datetime


class CourseViewSet(GenericViewSet,
                    ListModelMixin):
    queryset = Course.objects.all()
    filter_backends = [CoursesMobileFilterBackend]
    pagination_class = pagination.CustomPagination

    def filter_queryset(self, queryset):
        if self.request.query_params.get('age_group'):
            try:
                age_group = AgeGroup.objects.get(id=self.request.query_params.get('age_group'))
                queryset = queryset.filter(
                    Q(from_age__lte=age_group.to_age) | Q(to_age__gte=age_group.from_age)
                )
            except:
                pass
        if self.request.query_params.get('attendance_type'):
            queryset = queryset.filter(attendance_type=self.request.query_params.get('attendance_type'))
        if self.request.query_params.get('administrative_division'):
            queryset = queryset.filter(
                administrative_division__id=self.request.query_params.get('administrative_division')
            )
        if self.request.query_params.get('grade_group'):
            queryset = queryset.filter(grade_group__id=self.request.query_params.get('grade_type'))
        if self.request.query_params.get('grade_type'):
            queryset = queryset.filter(grade_type__id=self.request.query_params.get('grade_type'))
        if self.request.query_params.get('time'):
            if self.request.query_params.get('time') == constants.TIME_BEFORE_LUNCH:
                queryset = queryset.filter(weekdays__lesson_times__from_time__lte=datetime.time(hour=12, minute=0, second=0))
            elif self.request.query_params.get('time') == constants.TIME_AFTER_LUNCH:
                queryset = queryset.filter(
                    weekdays__lesson_times__from_time__gte=datetime.time(hour=12, minute=0, second=0))
        return queryset.distinct()

    # @action(detail=False, methods=['get'])
    # def test_data(self, request, pk=None):
    #     test_data.create_courses()
    #     return Response()

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseListSerializer
