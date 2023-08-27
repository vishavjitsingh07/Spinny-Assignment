""
import django_filters

from store.models import Cube


class CubeFilter(django_filters.FilterSet):
    length = django_filters.NumberFilter()
    length__gt = django_filters.NumberFilter(field_name="length", lookup_expr="gt")
    length__lt = django_filters.NumberFilter(field_name="length", lookup_expr="lt")

    width = django_filters.NumberFilter()
    width__gt = django_filters.NumberFilter(field_name="width", lookup_expr="gt")
    width__lt = django_filters.NumberFilter(field_name="width", lookup_expr="lt")

    height = django_filters.NumberFilter()
    height__gt = django_filters.NumberFilter(field_name="height", lookup_expr="gt")
    height__lt = django_filters.NumberFilter(field_name="height", lookup_expr="lt")

    area = django_filters.NumberFilter()
    area__gt = django_filters.NumberFilter(field_name="area", lookup_expr="gt")
    area__lt = django_filters.NumberFilter(field_name="area", lookup_expr="lt")

    volume = django_filters.NumberFilter()
    volume__gt = django_filters.NumberFilter(field_name="volume", lookup_expr="gt")
    volume__lt = django_filters.NumberFilter(field_name="volume", lookup_expr="lt")

    class Meta:
        model = Cube
        fields = []
