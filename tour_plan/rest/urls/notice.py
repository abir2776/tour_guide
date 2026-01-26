from django.urls import path

from tour_plan.rest.views.notice import NoticeDetailAPIView, NoticeListCreateAPIView

urlpatterns = [
    path("", NoticeListCreateAPIView.as_view(), name="notice-list-create"),
    path("<int:id>", NoticeDetailAPIView.as_view(), name="notice-details"),
]
