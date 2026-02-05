from rest_framework import serializers

from tour_plan.models import Image, Location, TourPlan
from tour_plan.rest.serializers.image import ImageSerializer
from tour_plan.rest.serializers.location import LocationSerializer


class TourPlanSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    image_ids = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), many=True, write_only=True, source="images"
    )
    location_ids = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), many=True, write_only=True, source="locations"
    )

    class Meta:
        model = TourPlan
        fields = "__all__"
