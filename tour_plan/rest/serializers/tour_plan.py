from rest_framework import serializers

from tour_plan.models import TourPlan


class TourPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPlan
        fields = "__all__"
