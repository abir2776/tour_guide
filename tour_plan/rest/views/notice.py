from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from tour_plan.models import Notice
from tour_plan.rest.serializers.notice import NoticeSerializer


class NoticeListCreateAPIView(ListCreateAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]
    queryset = Notice.objects.filter(is_active=True)
