from rest_framework import routers
from apps.sales.api.views import DeliveryViewSet, OrderViewSet, OrderDetailViewSet
from django.urls import path
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('delivery', DeliveryViewSet)
router.register('order', OrderViewSet)
router.register('order-details', OrderDetailViewSet)

urlpatterns = [
    path("", include(router.urls)),
]