from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data['bio'],
            profile_picture=validated_data.get('profile_picture', None)
        )
        Token.objects.create(user=user)
        return user


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)