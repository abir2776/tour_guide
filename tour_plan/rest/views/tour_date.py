from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import TourDate, TourPlan
from tour_plan.rest.serializers.tour_date import TourDateSerializer


class TourDateListCreateAPIView(ListCreateAPIView):
    serializer_class = TourDateSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        tour_id = self.kwargs.get("tour_id")
        return TourDate.objects.filter(tour_plan_id=tour_id)

    def perform_create(self, serializer):
        tour_id = self.kwargs.get("tour_id")
        tour_plan = TourPlan.objects.get(id=tour_id)
        serializer.save(tour_plan=tour_plan)


class TourDateRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TourDateSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        tour_id = self.kwargs.get("tour_id")
        return TourDate.objects.filter(tour_plan_id=tour_id)
