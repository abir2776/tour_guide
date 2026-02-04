from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from tour_plan.models import Location
from tour_plan.rest.serializers.location import LocationSerializer


class LocationListCreateAPIView(ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter()


class LocationDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter()
    lookup_field = "id"
