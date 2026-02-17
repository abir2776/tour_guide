from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField(required=False)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone", "password", "role"]

    def validate_email(self, data):
        email = data.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with email already exists!")
        return data

    def validate_phone(self, data):
        phone = data
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("User with phone already exists!")
        return data

    def create(self, validated_data, *args, **kwargs):
        email = validated_data["email"].lower()
        phone = validated_data.get("phone", None)
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        password = validated_data["password"]
        role = validated_data["role"]

        user = User.objects.create(
            email=email,
            username=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
            instance.save()
        return super().update(instance, validated_data)
