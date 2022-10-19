from rest_framework import routers
from apps.crm.api.views import CustomerCategoryViewSet, GetCustomerCategoryWithToken, DistrictViewSet, GetDistrictWithToken, Logout
from django.urls import path
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('customer-categories', CustomerCategoryViewSet)
router.register('district', DistrictViewSet)

urlpatterns = [
    path("", include(router.urls), name="api-crm"),
    path("customer-category/<int:id>/", GetCustomerCategoryWithToken.as_view(), name='get-customer-category'),
    path("district/<int:id>/", GetDistrictWithToken.as_view(), name='get-district-token'),
    path("logout/", Logout.as_view(), name="logout")
]