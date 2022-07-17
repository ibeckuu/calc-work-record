from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('item', views.ItemViewSet)
router.register('district', views.DistrictViewSet)
router.register('customer', views.CustomerViewSet)
router.register('order', views.OrderStatusViewSet)
router.register('inspect', views.InspectScheduleViewSet)
router.register('inspectrecord', views.InspectRecordViewSet)
router.register('inspectschedule', views.InspectScheduleViewSet)
router.register('inspectlist', views.InspectViewSet)
router.register('inspectqualified', views.InspectQualifiedViewSet)
router.register('inputorder', views.OrderStatusViewSet)
router.register('workingrecord', views.WorkingRecordViewSet)
router.register('otherevents', views.OtherEventsViewSet)
router.register('operator', views.OperatorViewSet)
router.register('inspect-monthly', views.InspectMonthlyViewSet)
router.register('shippingyearly', views.ShippingYearlyViewSet)
# router.register('aggregate-this-month-working', views.AggregateInspectThisMonthViewSet)

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls)),
]
