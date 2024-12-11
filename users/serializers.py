from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = get_user_model().objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # Используем username вместо email
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user
