from django.urls import include, path

urlpatterns = [
    path("plan/", include("tour_plan.rest.urls.tour_plan")),
    path("plan/date/", include("tour_plan.rest.urls.tour_date")),
    path("plan/date/time/", include("tour_plan.rest.urls.tour_time")),
    path("location/", include("tour_plan.rest.urls.location")),
    path("cart/", include("tour_plan.rest.urls.cart")),
    path("booking/", include("tour_plan.rest.urls.booking")),
    path("image/", include("tour_plan.rest.urls.image")),
    path("notice/", include("tour_plan.rest.urls.notice")),
]
