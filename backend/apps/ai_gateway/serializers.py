from rest_framework import serializers


class TextPayloadSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)


class SignPayloadSerializer(serializers.Serializer):
    image_base64 = serializers.CharField()
