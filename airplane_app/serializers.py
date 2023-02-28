from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from airplane_app.models import *


class BaseAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class BaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'is_active',
                  'is_superuser', 'email', 'first_name', 'last_name', 'is_staff']

        extra_kwargs = {
            "first_name": {
                "required": True,
            },
            "last_name": {
                "required": True,
            },
            "email": {
                "required": True,
                "validators": [
                    UniqueValidator(queryset=User.objects.all()),
                ],
            },
            "password": {"write_only": True, "required": True},
            "password_confirm": {"write_only": True, "required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise ValidationError({"password": "Password Fields must match."})
        try:
            validate_password(attrs["password"])
        except ValidationError as error:
            raise serializers.ValidationError({"password": error})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            is_staff=validated_data.get('is_staff'),
            is_superuser=validated_data.get('is_superuser'),
            is_active=validated_data.get('is_active')
        )
        user.set_password(password)
        user.save()
        return user


class ListFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        exclude = ["origin_country", ]


class CreateFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"

    def create(self, validated_data):
        return Flight.objects.create(**validated_data)


class DestroyFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["id", "flight_number"]


class RetrieveFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"
