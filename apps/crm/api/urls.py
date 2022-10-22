from rest_framework import routers
from apps.crm.api.views import CustomerCategoryViewSet, DistrictViewSet, CustomerViewSet
from django.urls import path
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('customer-categories', CustomerCategoryViewSet)
router.register('district', DistrictViewSet)
router.register('customer', CustomerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
