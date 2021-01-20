from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet \
    # , TelegramBotView

router = DefaultRouter()
router.register('courses', CourseViewSet)

urlpatterns = [
    # path('bot/', TelegramBotView.as_view())
]

urlpatterns += router.urls
