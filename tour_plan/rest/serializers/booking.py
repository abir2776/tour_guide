import decimal

from django.db import transaction
from rest_framework import serializers

from core.models import GuestUser,User
from tour_plan.models import Booking, BookingItem, CartItem


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = "__all__"
        read_only_fields = ["id","booking"]


class BookingSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    full_name = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(write_only=True, required=False)
    country = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    book_now = serializers.BooleanField(write_only=True, required=False)
    single_item = BookingItemSerializer(write_only=True, required=False)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["id","user","total_price"]

    def get_items(self, object):
        items = BookingItem.objects.filter(booking=object)
        return BookingItemSerializer(items, many=True).data
    
    def validate(self, attrs):
        status = attrs.get("status")
        cancelled_reason = attrs.get("cancelled_reason")

        if status == "cancelled" and (not cancelled_reason or len(cancelled_reason)<=0):
            raise serializers.ValidationError({
                "cancelled_reason": "Cancelled reason is required when status is cancelled."
            })

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
                booking = Booking.objects.create(
                    user=user, user_type=user_type, traveler_details=traveler_details
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
                        user=user,
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

            return booking
