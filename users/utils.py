from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


def get_tokens_for_user(user, password=None):
    refresh = RefreshToken.for_user(user)

    user = UserSerializer(user).data
    if password is not None:
        user['password'] = password

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': user
    }


