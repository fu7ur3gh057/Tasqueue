from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)

from apps.users.api.views import RegisterView, VerifyEmailView, LoginView, LogoutView, \
    UpdatePasswordView, RequestPasswordResetEmailView, PasswordTokenCheckView, SetNewPasswordView, \
    LoginView, delete_user_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/update/', UpdatePasswordView.as_view(), name='update-password'),
    # 3 step for resetting password
    path('reset/request/', RequestPasswordResetEmailView.as_view(), name='request-password'),
    path('reset/<uidb64>/<token>/', PasswordTokenCheckView.as_view(), name='token-check-password'),
    path('reset/set-password/', SetNewPasswordView.as_view(), name='set-password'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', delete_user_view, name='delete'),
]
