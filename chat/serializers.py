from rest_framework import serializers
from users.serializers import UserSerializer, FriendshipSerializer
from .models import Message, ChatRoom


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp')


class ChatRoomSerializer(serializers.ModelSerializer):
    friendship = FriendshipSerializer()
    
    class Meta:
        model = ChatRoom
        fields = ('uuid', 'friendship')