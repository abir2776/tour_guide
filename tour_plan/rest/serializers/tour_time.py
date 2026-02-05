from rest_framework import serializers

from tour_plan.models import TimeSlot
from tour_plan.rest.serializers.tour_date import TourDateSerializer


class TimeSlotSerializer(serializers.ModelSerializer):
    tour_date = TourDateSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = "__all__"
        read_only_fields = ("tour_date", "end_time")

    def validate(self, attrs):
        view = self.context.get("view")
        tour_date_id = view.kwargs.get("tour_date_id")
        start_time = attrs.get("start_time")

        qs = TimeSlot.objects.filter(
            tour_date_id=tour_date_id,
            start_time=start_time,
        )

        if qs.exists():
            raise serializers.ValidationError(
                {"start_time": "This start time already exists for this tour date."}
            )

        return attrs
