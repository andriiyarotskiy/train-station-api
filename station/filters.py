import django_filters

from station.models import Route


class RouteFilter(django_filters.FilterSet):
    min_distance = django_filters.NumberFilter(field_name="distance", lookup_expr="gte")
    max_distance = django_filters.NumberFilter(field_name="distance", lookup_expr="lte")

    class Meta:
        model = Route
        fields = ()
