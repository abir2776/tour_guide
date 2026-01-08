from rest_framework.generics import ListCreateAPIView

from tour_plan.models import Image
from tour_plan.rest.serializers.image import ImageSerializer


class ImageListCreateView(ListCreateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.filter()
