from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from station.models import TrainType, Train, Station, Route, Crew, Order, Trip
from station.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    TrainListSerializer,
    StationSerializer,
    RouteSerializer,
    CrewSerializer,
    OrderSerializer,
    TripSerializer,
    TripListSerializer,
    TripDetailSerializer,
    TrainDetailSerializer,
    OrderListSerializer,
)


class TrainTypeView(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        elif self.action == "retrieve":
            return TrainDetailSerializer
        return TrainSerializer

    def get_queryset(self):
        return Train.objects.select_related("train_type")


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    queryset = Trip.objects.select_related(
        "train__train_type", "route__source", "route__destination"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        elif self.action == "retrieve":
            return TripDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("crews")
        if self.action == "list":
            queryset = queryset.annotate(
                tickets_available=(
                    F("train__cargo_num") * F("train__places_in_cargo")
                    - Count("tickets")
                )
            )

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user")
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return self.serializer_class

    def get_queryset(self):
        qs = self.queryset

        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)

        if self.action in ("list", "retrieve"):
            qs = Order.objects.prefetch_related(
                "tickets__trip__train",
                "tickets__trip__route",
            )

        return qs

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ("destroy", "update", "partial_update"):
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
