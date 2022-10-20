from rest_framework import routers
from apps.sales.api.views import DeliveryViewSet, OrderViewSet, OrderDetailViewSet, GetDeliveryWithToken, GetOrderWithToken, GetOrderDetailWithToken
from django.urls import path
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('delivery', DeliveryViewSet)
router.register('order', OrderViewSet)
router.register('order-details', OrderDetailViewSet)

urlpatterns = [
    path("", include(router.urls), name="api-sales"),
    path("delivery/<int:id>/", GetDeliveryWithToken.as_view(), name='get-delivery'),
    path("order/<int:id>/", GetOrderWithToken.as_view(), name='get-order-token'),
    path("order-detail/<int:id>/", GetOrderDetailWithToken.as_view(), name='get-order-token')
]