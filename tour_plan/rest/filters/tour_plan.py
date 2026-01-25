import django_filters

from tour_plan.models import TourPlan


class TourPlanFilter(django_filters.FilterSet):
    price_adult = django_filters.RangeFilter()
    duration_days = django_filters.RangeFilter()

    class Meta:
        model = TourPlan
        fields = [
            "price_adult",
            "duration_days",
        ]
