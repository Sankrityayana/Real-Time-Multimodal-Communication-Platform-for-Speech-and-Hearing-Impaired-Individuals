from rest_framework import serializers

from .models import Message, Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'room_name', 'created_at', 'is_active']
        read_only_fields = ['id', 'room_name', 'created_at', 'is_active']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'session', 'sender', 'content', 'modality', 'created_at']
