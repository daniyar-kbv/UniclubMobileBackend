from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FilterDataViewSet

router = DefaultRouter()
router.register('filters', FilterDataViewSet)

urlpatterns = [
]

urlpatterns += router.urls
