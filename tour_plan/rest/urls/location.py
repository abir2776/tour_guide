from django.urls import path

from tour_plan.rest.views.location import LocationListCreateAPIView

urlpatterns = [
    path("", LocationListCreateAPIView.as_view(), name="location-list-create")
]
