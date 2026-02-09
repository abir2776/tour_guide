from django.urls import path

from tour_plan.rest.views.booking import (
    BookingItemDetails,
    BookingItemListCreate,
    BookingListCreateAPIView,
    BookingRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", BookingListCreateAPIView.as_view(), name="booking-list-create"),
    path(
        "<int:id>", BookingRetrieveUpdateDestroyAPIView.as_view(), name="booking-detail"
    ),
    path("items", BookingItemListCreate.as_view(), name="booking-item-list-create"),
    path("items/<int:id>", BookingItemDetails.as_view(), name="booking-item-details"),
]
