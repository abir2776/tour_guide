from django.urls import path

from core.rest.views.admin_token import AdminTokenView

urlpatterns = [path("", AdminTokenView.as_view(), name="admin-token-create")]
