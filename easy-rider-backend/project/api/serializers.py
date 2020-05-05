from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from project.api.models import Trip, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed'
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'user', 'destination', 'start_date', 'end_date', 'comment')
