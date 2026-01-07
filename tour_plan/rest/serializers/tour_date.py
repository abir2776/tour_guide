from rest_framework import serializers

from tour_plan.models import TourDate


class TourDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDate
        fields = "__all__"
        read_only_fields = ("tour_plan",)
