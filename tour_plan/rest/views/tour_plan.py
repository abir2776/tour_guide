from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from tour_plan.models import TourPlan
from tour_plan.rest.serializers.tour_plan import TourPlanSerializer


class TourPlanListCreateAPIView(ListCreateAPIView):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()


class TourPlanRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()
