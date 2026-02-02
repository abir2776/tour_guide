from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import Contact
from tour_plan.permissions import IsAdmin
from tour_plan.rest.filters.contacts import ContactFilter
from tour_plan.rest.serializers.contacts import ContactSerializer


class ContactListCreateAPIView(ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.filter()
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = ContactFilter

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class ContactDetailsView(RetrieveUpdateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.filter()
    permission_classes = [IsAdmin, IsAuthenticated]
    lookup_field = "id"
