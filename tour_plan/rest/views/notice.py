from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import Notice
from tour_plan.permissions import IsAdmin
from tour_plan.rest.serializers.notice import NoticeSerializer


class NoticeListCreateAPIView(ListCreateAPIView):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdmin()]
        return [AllowAny()]


class NoticeDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), IsAdmin()]
        return [AllowAny()]
