from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name']

    def create(self, validated_data):
        name = validated_data.pop('name')
        user = User(
            email=validated_data['email'],
            first_name=name,
            username=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
