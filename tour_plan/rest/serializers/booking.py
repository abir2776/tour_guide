import decimal

from django.db import transaction
from rest_framework import serializers

from core.models import GuestUser, User
from tour_plan.models import Booking, BookingItem, CartItem, TimeSlot
from tour_plan.rest.serializers.tour_plan import TourPlanSerializer
from tour_plan.rest.serializers.tour_time import TimeSlotSerializer


class BookingItemSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer(read_only=True)

    class Meta:
        model = BookingItem
        fields = "__all__"
        read_only_fields = ["id", "booking"]

    def validate(self, attrs):
        instance = self.instance
        if not instance:
            return attrs
        new_adults = attrs.get("num_adults", instance.num_adults)
        new_children = attrs.get("num_children", instance.num_children)
        new_infants = attrs.get("num_infants", instance.num_infants)
        new_youth = attrs.get("num_youth", instance.num_youth)
        new_student_eu = attrs.get("num_student_eu", instance.num_student_eu)
        diff_adults = new_adults - instance.num_adults
        diff_children = new_children - instance.num_children
        diff_infants = new_infants - instance.num_infants
        diff_youth = new_youth - instance.num_youth
        diff_student_eu = new_student_eu - instance.num_student_eu

        time_slot = instance.time_slot
        if (
            (diff_adults > 0 and time_slot.available_adults < diff_adults)
            or (diff_children > 0 and time_slot.available_children < diff_children)
            or (diff_infants > 0 and time_slot.available_infants < diff_infants)
            or (diff_youth > 0 and time_slot.available_youth < diff_youth)
            or (
                diff_student_eu > 0 and time_slot.available_student_eu < diff_student_eu
            )
        ):
            raise serializers.ValidationError(
                "Not enough availability in selected time slot."
            )

        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            time_slot = TimeSlot.objects.select_for_update().get(
                id=instance.time_slot.id
            )
            new_adults = validated_data.get("num_adults", instance.num_adults)
            new_children = validated_data.get("num_children", instance.num_children)
            new_infants = validated_data.get("num_infants", instance.num_infants)
            new_youth = validated_data.get("num_youth", instance.num_youth)
            new_student_eu = validated_data.get(
                "num_student_eu", instance.num_student_eu
            )
            diff_adults = new_adults - instance.num_adults
            diff_children = new_children - instance.num_children
            diff_infants = new_infants - instance.num_infants
            diff_youth = new_youth - instance.num_youth
            diff_student_eu = new_student_eu - instance.num_student_eu

            time_slot.available_adults -= diff_adults
            time_slot.available_children -= diff_children
            time_slot.available_infants -= diff_infants
            time_slot.available_youth -= diff_youth
            time_slot.available_student_eu -= diff_student_eu

            time_slot.save()

            return super().update(instance, validated_data)


class BookingItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = "__all__"
        read_only_fields = ["id", "booking"]


class BookingSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    full_name = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(write_only=True, required=False)
    country = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    book_now = serializers.BooleanField(write_only=True, required=False)
    single_item = BookingItemCreateSerializer(write_only=True, required=False)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["id", "user", "total_price"]

    def get_items(self, object):
        items = BookingItem.objects.filter(booking=object)
        return BookingItemSerializer(items, many=True).data

    def validate(self, attrs):
        status = attrs.get("status")
        cancelled_reason = attrs.get("cancelled_reason")

        if status == "cancelled" and (
            not cancelled_reason or len(cancelled_reason) <= 0
        ):
            raise serializers.ValidationError(
                {
                    "cancelled_reason": "Cancelled reason is required when status is cancelled."
                }
            )

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user_type = "guest"
            is_book_now = validated_data.pop("book_now", None)
            single_item = validated_data.pop("single_item", None)
            if self.context["request"].user.is_authenticated:
                user_type = "user"

            traveler_details = validated_data.pop("traveler_details")
            if user_type == "user":
                user = self.context["request"].user
                if user.role in ["ADMIN", "SUPER_ADMIN"]:
                    full_name = validated_data.pop("full_name")
                    email = validated_data.pop("email")
                    country = validated_data.pop("country")
                    phone = validated_data.pop("phone", None)
                    user = User.objects.filter(email=email)
                    if not user.exists():
                        guest_user = GuestUser.objects.create(
                            full_name=full_name,
                            email=email,
                            country=country,
                            phone=phone,
                        )
                        booking = Booking.objects.create(
                            guest_user=guest_user,
                            user_type="guest",
                            traveler_details=traveler_details,
                            booked_by_admin=True,
                        )
                    else:
                        booking = Booking.objects.create(
                            user=user.first(),
                            user_type="user",
                            traveler_details=traveler_details,
                            booked_by_admin=True,
                        )
                else:
                    booking = Booking.objects.create(
                        user=user,
                        user_type=user_type,
                        traveler_details=traveler_details,
                    )
                if not is_book_now:
                    cartitems = CartItem.objects.filter(user=user)
            else:
                full_name = validated_data.pop("full_name")
                email = validated_data.pop("email")
                country = validated_data.pop("country")
                phone = validated_data.pop("phone", None)
                user = User.objects.filter(email=email)
                if not user.exists():
                    guest_user = GuestUser.objects.create(
                        full_name=full_name, email=email, country=country, phone=phone
                    )
                    booking = Booking.objects.create(
                        guest_user=guest_user,
                        user_type="guest",
                        traveler_details=traveler_details,
                    )
                else:
                    booking = Booking.objects.create(
                        user=user.first(),
                        user_type="user",
                        traveler_details=traveler_details,
                    )
                if not is_book_now:
                    cart_item_ids = validated_data.pop("cart_item_ids")
                    cartitems = CartItem.objects.filter(id__in=cart_item_ids)

            if not is_book_now:
                total_price = decimal.Decimal(0)
                order_items_to_create = []
                for item in cartitems:
                    total_price += item.item_price
                    order_items_to_create.append(
                        BookingItem(
                            booking=booking,
                            tour_plan=item.tour_plan,
                            time_slot=item.time_slot,
                            num_adults=item.num_adults,
                            num_children=item.num_children,
                            num_infants=item.num_infants,
                            num_youth=item.num_youth,
                            num_student_eu=item.num_student_eu,
                            item_price=item.item_price,
                        )
                    )
                    item.time_slot.available_adults -= item.num_adults
                    item.time_slot.available_children -= item.num_children
                    item.time_slot.available_infants -= item.num_infants
                    item.time_slot.available_student_eu -= item.num_student_eu
                    item.time_slot.available_youth -= item.num_youth
                    item.time_slot.save()

                BookingItem.objects.bulk_create(order_items_to_create)
                cartitems.delete()
                booking.total_price = total_price
                booking.save()
            else:
                booking_item = BookingItem.objects.create(
                    booking=booking, **single_item
                )
                booking.total_price = booking_item.item_price
                booking.save()
                booking.time_slot.available_adults -= item.num_adults
                booking.time_slot.available_children -= item.num_children
                booking.time_slot.available_infants -= item.num_infants
                booking.time_slot.available_student_eu -= item.num_student_eu
                booking.time_slot.available_youth -= item.num_youth
                booking.time_slot.save()

            return booking


class BookingItemSerializerForBookinDetails(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer(read_only=True)
    tour_plan = TourPlanSerializer(read_only=True)

    class Meta:
        model = BookingItem
        fields = "__all__"
        read_only_fields = ["id", "booking", "tour_plan", "time_slot"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    full_name = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(write_only=True, required=False)
    country = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    book_now = serializers.BooleanField(write_only=True, required=False)
    single_item = BookingItemCreateSerializer(write_only=True, required=False)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["id", "user", "total_price"]

    def get_items(self, object):
        items = BookingItem.objects.filter(booking=object)
        return BookingItemSerializer(items, many=True).data

    def validate(self, attrs):
        status = attrs.get("status")
        cancelled_reason = attrs.get("cancelled_reason")

        if status == "cancelled" and (
            not cancelled_reason or len(cancelled_reason) <= 0
        ):
            raise serializers.ValidationError(
                {
                    "cancelled_reason": "Cancelled reason is required when status is cancelled."
                }
            )

        return attrs
