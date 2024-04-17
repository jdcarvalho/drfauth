from django.contrib.auth.models import User
from rest_framework import serializers
from app_api.models import Country


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'is_active', 'is_staff',
            'is_superuser', 'date_joined',
        ]


class UserLoginSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username = serializers.CharField(
        required=True,
    )

    password = serializers.CharField(
        required=True,
    )

