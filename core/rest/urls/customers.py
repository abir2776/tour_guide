from django.urls import path

from core.rest.views.customers import (
    CustomerBookingListAPIView,
    CustomerDetailsAPIView,
    CustomerListAPIView,
)

urlpatterns = [
    path("", CustomerListAPIView.as_view(), name="customer-list"),
    path("<int:id>", CustomerDetailsAPIView.as_view(), name="customer-details"),
    path(
        "<int:customer_id>/bookings",
        CustomerBookingListAPIView.as_view(),
        name="customer-booking-list",
    ),
]
