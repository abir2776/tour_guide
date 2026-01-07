from django.urls import path
from tour_plan.rest.views.tour_date import (
    TourDateListCreateAPIView,
    TourDateRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        '<int:tour_id>',
        TourDateListCreateAPIView.as_view(),
        name='tour-date-list-create'
    ),
    path(
        '<int:tour_id>/<int:pk>',
        TourDateRetrieveUpdateDestroyAPIView.as_view(),
        name='tour-date-detail'
    ),
]