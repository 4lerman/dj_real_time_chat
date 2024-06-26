from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q

from users.models import Friendship
from .models import ChatRoom
from .serializers import ChatRoomSerializer

User = get_user_model()


class ChatView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, receiver_id):
        user = self.request.user

        if not receiver_id:
            return Response({"error": "Receiver is not indicated"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        friendship = Friendship.objects.filter(
            Q(user1=user, user2=receiver) | Q(user1=receiver, user2=user)).first()

        if friendship is None:
            return Response({"error": "You are not friend with this user"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chat_room, created = ChatRoom.objects.get_or_create(
                friendship=friendship)

            serializer = ChatRoomSerializer(chat_room)
            # if serializer.is_valid():
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
