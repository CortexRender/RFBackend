from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from utils.response import RFResponse, ResponseCodes
from .models import RFUser
from .serializers import UserSerializer, RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return RFResponse(code=201, message='User registered successfully.', data=serializer.data,
                              status=status.HTTP_201_CREATED)
        return RFResponse(code=400, message='Validation failed.', errors=serializer.errors,
                          status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = RFUser.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return RFResponse(code=200, message='Login successful.', data=tokens, status=status.HTTP_200_OK)
        return RFResponse(code=401, message='Invalid credentials.',
                          errors={'error': 'Invalid username or password.'},
                          status=status.HTTP_401_UNAUTHORIZED)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return RFResponse(
                code=ResponseCodes.UNAUTHORIZED,
                message="User is not authenticated.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(request.user)
        return RFResponse(code=ResponseCodes.SUCCESS, message='User information retrieved.', data=serializer.data,
                          status=status.HTTP_200_OK)


class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return RFResponse(code=400, message='Email is required.', errors={'email': 'This field is required.'},
                              status=status.HTTP_400_BAD_REQUEST)

        try:
            user = RFUser.objects.get(email=email)
        except RFUser.DoesNotExist:
            return RFResponse(code=404, message='User not found.',
                              errors={'email': 'The email has not been registered.'}, status=status.HTTP_404_NOT_FOUND)

        username = user.username

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # reset_url = f"{request.scheme}://{request.get_host()}{reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})}"

        # separate React frontend URL:
        # reset_url = f"https://your-frontend.com/reset-password/{uid}/{token}"
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"


        email_body = render_to_string('email_templates/password_reset_email.html', {
            'reset_url': reset_url,
            'user': user,
            'username': username,
        })

        send_mail(
            subject='Password Reset Request',
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return RFResponse(code=200, message='Password reset link sent.', data={'email': email},
                          status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        new_password = request.data.get('password')
        if not new_password:
            return RFResponse(code=400, message='Password is required.', errors={'password': 'This field is required.'},
                              status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = RFUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return RFResponse(code=400, message='Invalid user.', errors={'user': 'User does not exist.'},
                              status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return RFResponse(code=400, message='Invalid token.',
                              errors={'token': 'The reset token is invalid or has expired.'},
                              status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        return RFResponse(code=200, message='Password has been reset successfully.', status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    permission_classes = []  # No authentication required

    def get(self, request):
        return RFResponse(code=200, message='Service is healthy.', data={'status': 'healthy'},
                          status=status.HTTP_200_OK)
