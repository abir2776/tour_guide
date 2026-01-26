from rest_framework.generics import ListAPIView, RetrieveAPIView

from core.models import User
from core.rest.serializers.customers import CustomerSerializer
from tour_plan.models import Booking
from tour_plan.permissions import IsAdmin
from tour_plan.rest.serializers.booking import BookingSerializer


class CustomerListAPIView(ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.filter(role="CUSTOMER")


class CustomerDetailsAPIView(RetrieveAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.filter(role="CUSTOMER")


class CustomerBookingListAPIView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        customer_id = self.kwargs.get("customer_id")
        return Booking.objects.filter(user_id=customer_id)
