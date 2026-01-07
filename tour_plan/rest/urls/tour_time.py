from django.urls import path

from tour_plan.rest.views.tour_time import (
    TimeSlotListCreateAPIView,
    TimeSlotRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "<int:tour_date_id>",
        TimeSlotListCreateAPIView.as_view(),
        name="time-slot-list-create",
    ),
    path(
        "<int:tour_date_id>/<int:pk>",
        TimeSlotRetrieveUpdateDestroyAPIView.as_view(),
        name="time-slot-detail",
    ),
]
