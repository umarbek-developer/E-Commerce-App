from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': {'id': user.id, 'email': user.email, 'name': user.get_full_name() or user.email},
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.get_full_name() or user.email,
                    'role': 'admin' if user.is_staff else 'customer',
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except KeyError:
            return Response({'detail': 'Refresh token required.'}, status=400)
        except Exception:
            return Response({'detail': 'Invalid or already blacklisted token.'}, status=400)
        return Response(status=status.HTTP_205_RESET_CONTENT)
