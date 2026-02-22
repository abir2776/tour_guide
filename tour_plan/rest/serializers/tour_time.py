from rest_framework import serializers

from tour_plan.models import TimeSlot
from tour_plan.rest.serializers.tour_date import TourDateSerializer


class TimeSlotSerializer(serializers.ModelSerializer):
    tour_date = TourDateSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = "__all__"
        read_only_fields = ("tour_date", "end_time")
