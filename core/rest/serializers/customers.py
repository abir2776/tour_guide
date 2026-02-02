from rest_framework import serializers

from core.models import User


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = "__all__"

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

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        instance.set_password(password)
        instance.save()
        return super().update(instance, validated_data)
