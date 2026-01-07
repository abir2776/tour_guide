from rest_framework import serializers

from tour_plan.models import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"
        read_only_fields = ("tour_date",)
