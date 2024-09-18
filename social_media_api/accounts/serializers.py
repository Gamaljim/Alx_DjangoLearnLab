from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class Register(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['bio', 'username', 'password', 'email']
