from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import TourPlan
from tour_plan.rest.filters.tour_plan import TourPlanFilter
from tour_plan.rest.serializers.tour_plan import TourPlanSerializer


class TourPlanListCreateAPIView(ListCreateAPIView):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]

    filterset_class = TourPlanFilter

    search_fields = [
        "title",
        "description",
        "locations__name",
    ]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]


class TourPlanRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TourPlanSerializer
    queryset = TourPlan.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]


class RecomandedTourPlanListCreateAPIView(ListAPIView):
    serializer_class = TourPlanSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        tour_id = self.kwargs.get("tour_id")
        return TourPlan.objects.exclude(id=tour_id).order_by("-id")[:8]
