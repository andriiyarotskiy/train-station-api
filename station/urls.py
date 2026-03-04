from django.urls import include, path
from rest_framework import routers

from station.views import TrainTypeView

router = routers.DefaultRouter()
router.register(r"train-types", TrainTypeView)

app_name = "station"

urlpatterns = [
    path("", include(router.urls)),
]
