from django.urls import path

from tour_plan.rest.views.contacts import ContactDetailsView, ContactListCreateAPIView

urlpatterns = [
    path("", ContactListCreateAPIView.as_view(), name="contact-list"),
    path("<int:id>", ContactDetailsView.as_view(), name="contact-details"),
]
