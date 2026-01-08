from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from tour_plan.models import CartItem
from tour_plan.rest.serializers.cart import CartItemSerializer


class CartItemListCreateAPIView(ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(user=self.request.user)
        super().perform_create(serializer)


class CartItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
