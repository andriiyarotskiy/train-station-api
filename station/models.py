from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.constraints import UniqueConstraint

from station_configs.settings import base as settings


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_from"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_to"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} - {self.destination.name} ({self.distance}km)"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)


class TrainType(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="trains"
    )

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Trip(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="trips")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="trips")
    crews = models.ManyToManyField(Crew, related_name="trips")

    class Meta:
        ordering = ("-departure_time",)

    def __str__(self):
        return f"{self.route} ({self.train})"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=["cargo", "seat", "trip"], name="unique_ticket_in_trip"
            ),
        )
        ordering = ("cargo", "seat")

    def __str__(self):
        return f"Cargo: {self.cargo}, Seat: {self.seat}"
