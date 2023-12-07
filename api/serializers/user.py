from datetime import datetime, timedelta, timezone
from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)


class SimpleMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)