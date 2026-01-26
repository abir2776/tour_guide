from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import Contact
from tour_plan.permissions import IsAdmin
from tour_plan.rest.serializers.contacts import ContactSerializer


class ContactListCreateAPIView(ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.filter()

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated(), IsAdmin()]


class ContactDetailsView(RetrieveAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.filter()
    permission_classes = [IsAdmin, IsAuthenticated]
