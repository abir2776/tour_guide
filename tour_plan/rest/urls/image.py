from django.urls import path

from tour_plan.rest.views.image import ImageDetailsView, ImageListCreateView

urlpatterns = [
    path("", ImageListCreateView.as_view(), name="image-list-create"),
    path("<int:pk>", ImageDetailsView.as_view(), name="image-details"),
]
