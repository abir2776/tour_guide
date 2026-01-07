from django.urls import path

from tour_plan.rest.views.booking import (
    BookingListCreateAPIView,
    BookingRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path(
        "<int:pk>", BookingRetrieveUpdateDestroyAPIView.as_view(), name="booking-detail"
    ),
]
