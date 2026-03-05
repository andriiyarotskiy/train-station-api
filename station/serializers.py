from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from station.models import TrainType, Station, Route, Order, Train, Crew, Trip, Ticket


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        source="source",
        queryset=Station.objects.all(),
        write_only=True,
    )

    destination = serializers.CharField(source="destination.name", read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(
        source="destination",
        queryset=Station.objects.all(),
        write_only=True,
    )

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Route.validate_route(
            attrs["source"].id,
            attrs["destination"].id,
            attrs["destination"],
            ValidationError,
        )
        return data

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "source_id",
            "destination",
            "destination_id",
            "distance",
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "capacity",
            "train_type",
        )


class TrainListSerializer(TrainSerializer):
    train_type = serializers.CharField(source="train_type.name", read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("id", "departure_time", "arrival_time", "route", "train", "crews")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "trip", "order")
