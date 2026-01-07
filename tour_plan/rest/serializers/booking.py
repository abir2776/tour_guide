import decimal

from django.db import transaction
from rest_framework import serializers

from tour_plan.models import Booking, BookingItem, CartItem


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = "__all__"
        read_only_fields = ("booking", "item_price")


class BookingSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = "__all__"

    def get_items(self, object):
        items = BookingItem.objects.filter(booking=object)
        return BookingItemSerializer(items, many=True).data

    def create(self, validated_data):
        with transaction.atomic:
            user = self.context["request"].user
            booking = Booking.objects.create(user=user)
            cartitems = CartItem.objects.filter(user=user)
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
            booking.total_price = total_price
            booking.save()
            return booking
