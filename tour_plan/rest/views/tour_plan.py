from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import TourPlan
from tour_plan.rest.serializers.tour_plan import TourPlanSerializer


class TourPlanListCreateAPIView(ListCreateAPIView):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]


class TourPlanRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()

    def get_permissions(self):
        return [AllowAny()]


class RecomandedTourPlanListCreateAPIView(ListAPIView):
    serializer_class = TourPlanSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        tour_id = self.kwargs.get("tour_id")
        return TourPlan.objects.filter().exclude(tour_id=tour_id)
