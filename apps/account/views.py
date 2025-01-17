from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import UserResetPasswordToken
from .serializers import RegisterSerializer, LogoutSerializer, ResetPasswordSerializer, ResetPasswordConfirmSerializer

from apps.generals.send_mail import send_activation_email, send_reset_password_email
from apps.generals.generate_reset_token import generate_reset_password_token
from .tasks import send_reset_password_email_task, send_activation_email_task

User = get_user_model()
class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            try:
                send_activation_email_task.delay(email=user.email, code=user.activation_code)
            except Exception as e:
                return Response({
                    "msg": "Error while sending email",
                    "data": serializer.data,
                })
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    def get(self, request):
        activation_code = request.query_params.get('u')
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response({
            "msg": "User activated",
        }, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny, ]

class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny, ]

class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"msg": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"msg": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        reset_code = generate_reset_password_token()
        UserResetPasswordToken.objects.create(user=user, token=reset_code)
        send_reset_password_email_task.delay(
            email=email,
            code=reset_code,)
        return Response({"msg": "Password reset email sent"}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        code = request.data.get('code')
        password = request.data.get('password')

        try:
            reset_code = UserResetPasswordToken.objects.get(token=code)
        except UserResetPasswordToken.DoesNotExist:
            return Response({"msg": "Reset code does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_code.is_valid():
            return Response({"msg": "Reset code has expired"}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_code.user
        user.set_password(password)
        user.save()
        reset_code.delete()
        return Response({"msg": "Password reset successfully"}, status=status.HTTP_200_OK)