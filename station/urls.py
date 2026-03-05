from django.urls import include, path
from rest_framework import routers

from station.views import (
    TrainTypeView,
    TrainViewSet,
    StationViewSet,
    RouteViewSet,
    CrewViewSet,
    OrderViewSet,
    TripViewSet,
)

router = routers.DefaultRouter()
router.register(r"train-types", TrainTypeView)
router.register(r"trains", TrainViewSet)
router.register(r"stations", StationViewSet)
router.register(r"routes", RouteViewSet)
router.register(r"crews", CrewViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"trips", TripViewSet)

app_name = "station"

urlpatterns = [
    path("", include(router.urls)),
]
