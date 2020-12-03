from django.db.models import Q

from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
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
from utils.telegrambot import bot

import constants, datetime, telebot


class CourseViewSet(GenericViewSet,
                    ListModelMixin):
    queryset = Course.objects.all()
    filter_backends = [CoursesMobileFilterBackend]
    pagination_class = pagination.CustomPagination

    def filter_queryset(self, queryset):
        if self.request.query_params.getlist('age_groups[]'):
            for index, age_group_id in enumerate(self.request.query_params.getlist('age_groups[]')):
                try:
                    age_group = AgeGroup.objects.get(id=age_group_id)
                    new_q = queryset.filter(
                        Q(from_age__lte=age_group.to_age) | Q(to_age__gte=age_group.from_age)
                    )
                    if index == 0:
                        q = new_q
                    else:
                        q = q | new_q
                except:
                    pass
            queryset = q
        if self.request.query_params.getlist('attendance_types[]'):
            queryset = queryset.filter(attendance_type_id__in=self.request.query_params.getlist('attendance_types[]'))
        if self.request.query_params.getlist('administrative_divisions[]'):
            queryset = queryset.filter(
                administrative_division_id__in=self.request.query_params.getlist('administrative_divisions[]')
            )
        if self.request.query_params.getlist('grade_groups[]'):
            queryset = queryset.filter(grade_group_id__in=self.request.query_params.getlist('grade_groups[]'))
        if self.request.query_params.getlist('grade_types[]'):
            queryset = queryset.filter(grade_type_id__in=self.request.query_params.getlist('grade_types[]'))
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


class TelegramBotView(APIView):
    def post(self, request, format=None):
        json_string = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return Response()
