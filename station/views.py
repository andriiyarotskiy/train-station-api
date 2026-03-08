from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from station.filters import RouteFilter
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
    StationImageSerializer,
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

    def get_serializer_class(self):
        if self.action == "upload_image":
            return StationImageSerializer
        return StationSerializer

    @action(detail=True, methods=["post"], url_path="upload-image")
    def upload_image(self, request, pk=None):
        station = self.get_object()
        serializer = self.get_serializer(station, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RouteFilter


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ("create", "destroy", "update", "partial_update"):
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]


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
            qs = qs.prefetch_related(
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
