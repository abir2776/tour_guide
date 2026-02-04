from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.rest.serializers.admin_token import AdminLoginSerializer


class AdminTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
