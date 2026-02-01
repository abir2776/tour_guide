from django.urls import include, path

urlpatterns = [
    path("register/", include("core.rest.urls.register")),
    path("users/", include("core.rest.urls.users")),
]
