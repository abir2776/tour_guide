from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from tour_plan.models import CartItem
from tour_plan.rest.serializers.cart import CartItemSerializer


class CartItemListCreateAPIView(ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [AllowAny()]

    def get_queryset(self):
        cart_ids = self.request.query_params.get("cart_ids")

        if not cart_ids:
            raise ValidationError({"cart_ids": "This query parameter is required."})

        try:
            cart_ids = [int(cid) for cid in cart_ids.split(",")]
        except ValueError:
            raise ValidationError(
                {"cart_ids": "cart_ids must be a comma-separated list of integers."}
            )

        return CartItem.objects.filter(id__in=cart_ids)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class CartItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_permissions(self):
        return [AllowAny()]
