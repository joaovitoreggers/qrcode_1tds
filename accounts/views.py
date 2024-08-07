from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
import logging
from .serializers import SetNewPasswordSerializer, UserModelSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken


logger = logging.getLogger(__name__)


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class UserRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class PasswordResetView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Email não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_data = {
                'uidb64': uidb64,
                'token': token,
            }
            self.send_reset_email(user.email, reset_data)
            logger.info(f'Password reset email sent to {email}')
            return Response({'message': 'Instruções para a alteração da senha foram enviadas para o seu email'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_reset_email(self, email, reset_data):
        send_mail(
            'Password Reset Request',
            f'Use este token e User ID para resetar a Senha(enquanto não tem front): {reset_data}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                logger.error('Invalid user ID or user not found')
                return Response({'error': 'Token, ou ID de usuário inválidos'}, status=status.HTTP_400_BAD_REQUEST)

            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(password)
                user.save()
                logger.info(f'Password reset for user {user.username}')
                return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)
            else:
                logger.error('Invalid token')
                return Response({'error': 'Token, ou ID de usuário inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtém o nome de usuário e a senha do corpo da requisição
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Autentica o usuário
        user = authenticate(username=username, password=password)
        
        if user:
            # Se a autenticação for bem-sucedida, cria um token JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            # Se a autenticação falhar, retorna um erro 401
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    