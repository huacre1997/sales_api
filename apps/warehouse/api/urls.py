from rest_framework import routers
from apps.warehouse.api.views import ProductCategoryViewSet
from django.urls import path
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('product-categories', ProductCategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
