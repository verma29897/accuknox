from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import FriendRequest
from django.utils import timezone
from datetime import timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'].lower(),
            email=validated_data['email'].lower(),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'is_accepted', 'timestamp']

class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['to_user']

    def validate(self, data):
        user = self.context['request'].user
        to_user = data['to_user']

        if FriendRequest.objects.filter(from_user=user, to_user=to_user).exists():
            raise serializers.ValidationError("Friend request already sent.")
        
        recent_requests = FriendRequest.objects.filter(
            from_user=user,
            timestamp__gte=timezone.now() - timedelta(minutes=1)
        )

        if recent_requests.count() >= 3:
            raise serializers.ValidationError("You cannot send more than 3 friend requests within a minute.")

        return data
