from django.urls import include, path
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("users/", include('users.urls')),
    path("chat/", include('chat.urls')),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

]
