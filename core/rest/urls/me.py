from django.urls import path

from core.rest.views.me import MeAPIView

urlpatterns = [path("", MeAPIView.as_view(), name="my-profile")]
