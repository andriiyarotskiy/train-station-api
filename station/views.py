from rest_framework import viewsets

from station.models import TrainType
from station.serializers import TrainTypeSerializer


class TrainTypeView(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
