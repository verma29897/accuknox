# accounts/urls.py

from django.urls import path
from .views import (
    UserSignupView, UserLoginView, UserSearchView,
    FriendRequestCreateView, FriendRequestResponseView,
    FriendsListView, PendingFriendRequestsView
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestCreateView.as_view(), name='friend-request'),
    path('friend-request/<int:pk>/response/', FriendRequestResponseView.as_view(), name='friend-request-response'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
