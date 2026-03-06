from django.db import transaction
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


class TrainDetailSerializer(serializers.HyperlinkedModelSerializer):
    train_type = serializers.CharField(source="train_type.name", read_only=True)

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "capacity",
            "train_type",
            "url",
        )
        extra_kwargs = {
            "url": {"view_name": "station:train-detail", "lookup_field": "pk"}
        }


class TrainListSerializer(TrainSerializer):
    train_type = serializers.CharField(source="train_type.name", read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class TripSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if attrs["departure_time"] > attrs["arrival_time"]:
            raise ValidationError(
                {"departure_time": "Departure time must be before arrival time."}
            )
        return validated_data

    class Meta:
        model = Trip
        fields = ("id", "departure_time", "arrival_time", "route", "train", "crews")


class TripListSerializer(TripSerializer):
    route = serializers.StringRelatedField(read_only=True)
    train = TrainDetailSerializer(read_only=True)
    tickets_available = serializers.CharField(read_only=True)

    class Meta:
        model = Trip
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "train",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super().validate(attrs=attrs)

        return data

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "trip")


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("cargo", "seat")


class TripDetailSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    train = TrainListSerializer(read_only=True)
    crews = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )

    # Another approach is to simply show the number of seats occupied
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation["taken_places"] = instance.tickets.count()
    #
    #     return representation

    taken_places = TicketSeatsSerializer(read_only=True, many=True, source="tickets")

    class Meta:
        model = Trip
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "train",
            "crews",
            "taken_places",
        )


class TicketListSerializer(TicketSerializer):
    trip = TripListSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    @transaction.atomic
    def create(self, validated_data):
        tickets = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket in tickets:
            Ticket.objects.create(order=order, **ticket)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        tickets_data = validated_data.pop("tickets")
        instance.tickets.all().delete()

        for ticket in tickets_data:
            Ticket.objects.create(order=instance, **ticket)
        instance.save()
        return instance


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


# {
#     "tickets": [
#         {
#             "cargo": 1,
#             "seat": 1,
#             "trip": 1
#         }
#     ]
# }
