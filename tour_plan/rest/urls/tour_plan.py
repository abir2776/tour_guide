from django.urls import path

from tour_plan.rest.views.tour_plan import (
    TourPlanListCreateAPIView,
    TourPlanRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "", TourPlanListCreateAPIView.as_view(), name="tour-plan-list-create"
    ),
    path(
        "<int:pk>",
        TourPlanRetrieveUpdateDestroyAPIView.as_view(),
        name="tour-plan-detail",
    ),
]
