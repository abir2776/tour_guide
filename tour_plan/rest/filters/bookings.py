import django_filters

from tour_plan.models import Booking


class BookingFilter(django_filters.FilterSet):
    category = django_filters.BaseInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = Booking
        fields = ["status"]
