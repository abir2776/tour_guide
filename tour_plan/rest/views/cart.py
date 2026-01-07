from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from tour_plan.models import CartItem
from tour_plan.rest.serializers.cart import (
    CartItemSerializer,
)


class CartItemListCreateAPIView(ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
