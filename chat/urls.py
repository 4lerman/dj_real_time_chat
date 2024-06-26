from django.urls import path
from .views import ChatView


urlpatterns = [
    path('<int:receiver_id>/', ChatView.as_view(), name='chat'),
]
