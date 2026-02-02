from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from tour_plan.models import Booking, Contact, TourPlan


class DashboardStatsAPIView(APIView):
    def get(self, request):
        contact_stats = Contact.objects.aggregate(
            pending=Count(
                "id",
                filter=Q(status__in=["open", "in_review"]),
            ),
            cancelled=Count(
                "id",
                filter=Q(status="cancelled"),
            ),
            completed=Count(
                "id",
                filter=Q(status="completed"),
            ),
            total=Count("id"),
        )

        booking_stats = Booking.objects.aggregate(
            pending=Count(
                "id",
                filter=Q(status__in=["open", "in_review"]),
            ),
            accepted=Count(
                "id",
                filter=Q(status="accepted"),
            ),
            cancelled=Count(
                "id",
                filter=Q(status="cancelled"),
            ),
            completed=Count(
                "id",
                filter=Q(status="completed"),
            ),
            total=Count("id"),
        )
        total_plan = TourPlan.objects.filter().count()

        return Response(
            {
                "contacts": contact_stats,
                "bookings": booking_stats,
                "total_tour_plan": total_plan,
            }
        )
