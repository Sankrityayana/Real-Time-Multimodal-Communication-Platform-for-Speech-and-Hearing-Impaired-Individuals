from rest_framework import serializers


class TextPayloadSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)
    session_id = serializers.UUIDField(required=False)


class SignPayloadSerializer(serializers.Serializer):
    image_base64 = serializers.CharField()
    session_id = serializers.UUIDField(required=False)
