from django.urls import path

from core.rest.views.users import UserDetailsApiVew, UserListCreateApiView

urlpatterns = [
    path("", UserListCreateApiView.as_view(), name="user-list"),
    path("<int:id>", UserDetailsApiVew.as_view(), name="user-details"),
]
