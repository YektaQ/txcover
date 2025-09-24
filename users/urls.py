from django.urls import path
from django.shortcuts import redirect

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView , GetTokenView ,phone_auth_view

urlpatterns = [
    path('', lambda request: redirect('phone_auth')),

    path('register/', RegisterView.as_view(), name='register'),
    path('token/', GetTokenView.as_view(), name='token'),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('phone_auth/', phone_auth_view, name='phone_auth'),
]