from django.db import models
from django.contrib.auth import get_user_model
from users.models import Friendship
import uuid

# Create your models here.

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver}"


class ChatRoom(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    friendship = models.ForeignKey(Friendship, on_delete=models.CASCADE)
