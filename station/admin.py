from django.contrib import admin
from django.contrib.auth.models import Group

from station.models import Station, Ticket, Order, Route, Train, Crew, TrainType, Trip


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(Train)
admin.site.register(Crew)
admin.site.register(TrainType)
admin.site.register(Trip)

admin.site.unregister(Group)
