from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from tour_plan.models import TimeSlot, TourDate
from tour_plan.rest.serializers.tour_time import (
    TimeSlotSerializer,
)


class TimeSlotListCreateAPIView(ListCreateAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        tour_date_id = self.kwargs.get("tour_date_id")
        return TimeSlot.objects.filter(tour_date_id=tour_date_id)

    def perform_create(self, serializer):
        tour_date_id = self.kwargs.get("tour_date_id")
        tour_date = TourDate.objects.get(id=tour_date_id)
        serializer.save(tour_date=tour_date)


class TimeSlotRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        tour_date_id = self.kwargs.get("tour_date_id")
        return TimeSlot.objects.filter(tour_date_id=tour_date_id)
