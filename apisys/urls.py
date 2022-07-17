from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('matters', views.MatterViewSet)

app_name = 'apisys'
urlpatterns = [
    path('', include(router.urls)),
]
