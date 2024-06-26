from django.urls import path
from .views import RegisterView, LoginView, ActivateView, SendFriendRequestView


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('friend_request', SendFriendRequestView.as_view(),
         name='friend_request')
]
