from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from tour_plan.models import Booking
from tour_plan.rest.serializers.booking import BookingSerializer


class BookingListCreateAPIView(ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
