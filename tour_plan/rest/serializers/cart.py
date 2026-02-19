from rest_framework import serializers

from tour_plan.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ("user", "item_price")

    def validate(self, attrs):
        time_slot = attrs.get("time_slot")
        tour_plan = attrs.get("tour_plan")

        num_adults = attrs.get("num_adults", 0)
        num_children = attrs.get("num_children", 0)
        num_infants = attrs.get("num_infants", 0)
        num_youth = attrs.get("num_youth", 0)
        num_student_eu = attrs.get("num_student_eu", 0)
        if self.instance:
            num_adults = attrs.get("num_adults", self.instance.num_adults)
            num_children = attrs.get("num_children", self.instance.num_children)
            num_infants = attrs.get("num_infants", self.instance.num_infants)
            num_youth = attrs.get("num_youth", self.instance.num_youth)
            num_student_eu = attrs.get("num_student_eu", self.instance.num_student_eu)
            time_slot = attrs.get("time_slot", self.instance.time_slot)

        if not time_slot.has_availability(
            adults=num_adults,
            children=num_children,
            infants=num_infants,
            youth=num_youth,
            student_eu=num_student_eu,
        ):
            raise serializers.ValidationError(
                "Selected time slot does not have enough availability."
            )

        return attrs
