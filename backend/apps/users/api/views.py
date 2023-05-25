import os

import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status, views, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from .serializers import *


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [{os.environ.get("APP_SCHEME", "")}, 'http', 'https']


def get_client_ip(request: Request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR')


# Registration
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # renderer_classes = (UserRenderer,)

    def post(self, request: Request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        # user access token
        token = RefreshToken.for_user(user).access_token
        frontend_url = 'http://localhost:3000/auth/verify/'
        full_url = f'{frontend_url}/{token}'
        email_body = f'Hi {user.email}, use link below to verify\n{full_url}'
        data = {'email_body': email_body, 'email_subject': 'Verify your email', 'receivers': user.email}
        # make a celery task
        # send_email_task.delay(data)
        return Response(user_data, status.HTTP_201_CREATED)


# Login
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# Email Verification
class VerifyEmailView(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request: Request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer

    def update(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if hasattr(user, ''):
        #     user.delete()
        return Response({'Success': True}, status=status.HTTP_200_OK)


class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request: Request):
        # serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        user = User.objects.filter(email=email).first()
        if user is not None:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.pkid))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('token-check-password', kwargs={'uidb64': uidb64, 'token': token})
            redirect_url = request.data.get('redirect_url', '')
            full_url = f'http://{current_site}{relative_link}'
            email_body = f'Hello {user.email}, Use link below to reset your password\n{full_url}{redirect_url}'
            data = {'email_subject': 'Reset your password', 'email_body': email_body, 'receivers': user.email}
            # celery task
            # send_email_task.delay(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request: Request, uidb64, token):
        frontend_url = f'{os.environ.get("FRONTEND_URL", "")}/auth/set-password/'
        # redirect_url = request.GET.get('redirect_url')
        redirect_url = frontend_url
        try:
            pkid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pkid=pkid)
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(f'{frontend_url}?token_valid=False')
                else:
                    return CustomRedirect(f'{frontend_url}?token_valid=False')
            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    f'{redirect_url}?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}')
            else:
                return CustomRedirect(f'{frontend_url}?token_valid=False')
        except DjangoUnicodeDecodeError as error:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(f'{redirect_url}?token_valid=False')
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


# Not Works
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user_view(request: Request):
    print('salam')
    return Response('salam')
