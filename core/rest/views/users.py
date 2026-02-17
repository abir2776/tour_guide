from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from core.choices import UserRole
from core.models import User
from core.permissions import IsSuperUser
from core.rest.serializers.users import UserSerializer


class UserListCreateApiView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    queryset = User.objects.filter(role=UserRole.ADMIN)


class UserDetailsApiVew(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    queryset = User.objects.filter(role=UserRole.ADMIN)
    lookup_field = "id"
