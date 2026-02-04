from django.urls import path

from tour_plan.rest.views.location import LocationDetailsView, LocationListCreateAPIView

urlpatterns = [
    path("", LocationListCreateAPIView.as_view(), name="location-list-create"),
    path("<int:id>", LocationDetailsView.as_view(), name="location-details"),
]
