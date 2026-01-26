from rest_framework.generics import RetrieveUpdateDestroyAPIView

from core.rest.serializers.customers import CustomerSerializer


class MeAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer

    def get_object(self):
        return self.request.user
