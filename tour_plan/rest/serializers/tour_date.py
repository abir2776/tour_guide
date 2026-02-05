from rest_framework import serializers

from tour_plan.models import TourDate


class TourDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDate
        fields = "__all__"
        read_only_fields = ("tour_plan",)

    def validate(self, attrs):
        request = self.context.get("request")
        view = self.context.get("view")

        tour_id = view.kwargs.get("tour_id")
        date = attrs.get("date")

        if TourDate.objects.filter(tour_plan_id=tour_id, date=date).exists():
            raise serializers.ValidationError(
                {"date": "This date already exists for this tour."}
            )

        return attrs
