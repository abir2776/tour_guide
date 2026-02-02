from django.urls import path

from tour_plan.rest.views.dashboard import DashboardStatsAPIView

urlpatterns = [path("", DashboardStatsAPIView.as_view(), name="dashboard")]
