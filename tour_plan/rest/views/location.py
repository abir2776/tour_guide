from rest_framework.generics import ListCreateAPIView

from tour_plan.models import Location
from tour_plan.rest.serializers.location import LocationSerializer


class LocationListCreateAPIView(ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter()
