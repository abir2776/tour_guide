from django.urls import path

from tour_plan.rest.views.notice import NoticeListCreateAPIView

urlpatterns = [path("", NoticeListCreateAPIView.as_view(), name="notice-list-create")]
