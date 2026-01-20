from django.urls import path

from tour_plan.rest.views.tour_plan import (
    RecomandedTourPlanListCreateAPIView,
    TourPlanListCreateAPIView,
    TourPlanRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", TourPlanListCreateAPIView.as_view(), name="tour-plan-list-create"),
    path(
        "<int:pk>",
        TourPlanRetrieveUpdateDestroyAPIView.as_view(),
        name="tour-plan-detail",
    ),
    path(
        "recomended/<int:tour_id>",
        RecomandedTourPlanListCreateAPIView.as_view(),
        name="recomanded-tour-plan-list",
    ),
]
