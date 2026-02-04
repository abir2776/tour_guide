from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "No account found with this email"}
            )
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid credentials"})
        if user.role not in ["ADMIN", "SUPER_ADMIN"]:
            raise serializers.ValidationError(
                {"detail": "You are not allowed to access this resource"}
            )
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
