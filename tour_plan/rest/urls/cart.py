from django.urls import path

from tour_plan.rest.views.cart import (
    CartItemListCreateAPIView,
    CartItemRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", CartItemListCreateAPIView.as_view(), name="cart-item-list-create"),
    path(
        "<int:pk>",
        CartItemRetrieveUpdateDestroyAPIView.as_view(),
        name="cart-item-detail",
    ),
]
