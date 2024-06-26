from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .tasks import send_activation_email
from .utils import get_tokens_for_user
from .serializers import RegisterSerializer, FriendRequestSerializer
from .models import FriendRequest, Friendship
from chat.models import ChatRoom

User = get_user_model()

# Create your views here.


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            request_data = request._request

            send_activation_email(user, request_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):

        data = request.data

        if "email" not in data and "username" not in data:
            return Response({
                "error": "Email or username is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        if "password" not in data.keys():
            return Response({
                "error": "Password is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(
            Q(email=email) | Q(username=username)).first()

        if user and user.check_password(password):
            if not user.is_active:
                return Response({"error": "Account is not activated. Please check your email."}, status=status.HTTP_403_FORBIDDEN)
            data = get_tokens_for_user(user)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "User does not exist or activation required"
            }, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"success": "Account activated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Activation link is invalid"}, status=status.HTTP_400_BAD_REQUEST)


class SendFriendRequestView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = self.request.user

        sent_friend_requests = FriendRequest.objects.filter(from_user=user)
        received_friend_requests = FriendRequest.objects.filter(to_user=user)\

        sent_serializer = FriendRequestSerializer(
            sent_friend_requests, many=True)
        received_serializer = FriendRequestSerializer(
            received_friend_requests, many=True)

        return Response({
            'sent_requests': sent_serializer.data,
            'received_requests': received_serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        from_user = self.request.user
        data = request.data

        if 'to_user' not in data.keys():
            return Response({"error": "Please indicate user to send friend request"}, status=status.HTTP_400_BAD_REQUEST)

        to_user_id = data['to_user']

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if from_user.id == to_user_id:
            return Response({"error": "Cannot send friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=to_user, to_user=from_user).exists():
            return Response({"error": "Friend request already received from this user"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()

        serializer = FriendRequestSerializer(friend_request)

        response_data = {}
        response_data['data'] = serializer.data
        response_data['message'] = 'Friend Request Succesfuly sent'

        return Response(response_data, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = self.request.user

        data = request.data
        if "from_user" not in data:
            return Response({"error": "Please indicate user"}, status=status.HTTP_400_BAD_REQUEST)
        if 'status' not in data:
            return Response({"error": "Please indicate the status"}, status=status.HTTP_400_BAD_REQUEST)

        from_user_id = data['from_user']
        response_to_fr = data['status']
        from_user = User.objects.get(id=from_user_id)

        valid_statuses = ['pending', 'accepted', 'declined']
        if response_to_fr not in valid_statuses:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(
                from_user=from_user, to_user=user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "No friend request from " + from_user.username}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = response_to_fr
        friend_request.save()

        if response_to_fr == 'accepted':
            friendship = Friendship(user1=from_user, user2=user)
            friendship.save()

        serializer = FriendRequestSerializer(friend_request)

        return Response(serializer.data, status=status.HTTP_200_OK)
