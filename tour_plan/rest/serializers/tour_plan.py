from rest_framework import serializers

from tour_plan.models import TourPlan
from tour_plan.rest.serializers.image import ImageSerializer
from tour_plan.rest.serializers.location import LocationSerializer


class TourPlanSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = TourPlan
        fields = "__all__"
