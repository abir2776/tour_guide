from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import Booking
from tour_plan.rest.serializers.booking import BookingSerializer


class BookingListCreateAPIView(ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
