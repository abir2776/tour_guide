from django.urls import path

from tour_plan.rest.views.image import ImageListCreateView

urlpatterns = [path("", ImageListCreateView.as_view(), name="image-list-create")]
