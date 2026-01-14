import decimal

from django.db import transaction
from rest_framework import serializers

from core.models import GuestUser
from tour_plan.models import Booking, BookingItem, CartItem


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = "__all__"
        read_only_fields = ("booking", "item_price")


class BookingSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    full_name = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(write_only=True, required=False)
    country = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = []

    def get_items(self, object):
        items = BookingItem.objects.filter(booking=object)
        return BookingItemSerializer(items, many=True).data

    def create(self, validated_data):
        with transaction.atomic():
            user_type = "guest"
            if self.context["request"].user.is_authenticated:
                user_type = "user"

            traveler_details = validated_data.pop("traveler_details")
            if user_type == "user":
                user = self.context["request"].user
                booking = Booking.objects.create(
                    user=user, user_type=user_type, traveler_details=traveler_details
                )
                cartitems = CartItem.objects.filter(user=user)
            else:
                full_name = validated_data.pop("full_name")
                email = validated_data.pop("email")
                country = validated_data.pop("country")
                phone = validated_data.pop("phone")
                cart_item_ids = validated_data.pop("cart_item_ids")
                guest_user = GuestUser.objects.create(
                    full_name=full_name, email=email, country=country, phone=phone
                )
                booking = Booking.objects.create(
                    guest_user=guest_user,
                    user_type="guest",
                    traveler_details=traveler_details,
                )
                cartitems = CartItem.objects.filter(id__in=cart_item_ids)

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
                        item_price=item.item_price,
                    )
                )

            BookingItem.objects.bulk_create(order_items_to_create)
            cartitems.delete()
            booking.total_price = total_price
            booking.save()
            return booking
