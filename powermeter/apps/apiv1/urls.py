from django.urls import include, path
from rest_framework import routers

from .views import DeviceViewSet, MeteringViewSet


router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'meterings', MeteringViewSet)

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls)),
]
