from django.shortcuts import render
# accounts/views.py

from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import FriendRequest
from .serializers import (
    UserSerializer, LoginSerializer,
    FriendRequestSerializer, FriendRequestCreateSerializer
)

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

class UserSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        search_keyword = self.request.query_params.get('q', '').lower()
        if '@' in search_keyword:
            return User.objects.filter(email__iexact=search_keyword)
        else:
            return User.objects.filter(username__icontains=search_keyword)

class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestCreateSerializer

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class FriendRequestResponseView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get('action')

        if action == 'accept':
            instance.is_accepted = True
            instance.save()
            return Response({'status': 'Friend request accepted'})
        elif action == 'reject':
            instance.delete()
            return Response({'status': 'Friend request rejected'})
        return Response({'status': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(sent_requests__to_user=user, sent_requests__is_accepted=True)

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, is_accepted=False)
