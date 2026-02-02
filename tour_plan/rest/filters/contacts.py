import django_filters

from tour_plan.models import Contact


class ContactFilter(django_filters.FilterSet):
    category = django_filters.BaseInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = Contact
        fields = ["status"]
