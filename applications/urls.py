from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookingApplicationViewSet, PartnershipApplicationViewSet

router = DefaultRouter()
router.register('booking', BookingApplicationViewSet)
router.register('partnership', PartnershipApplicationViewSet)

urlpatterns = [
]

urlpatterns += router.urls
