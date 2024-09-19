from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, TokenSerializer, ProfileSerializer, FollowSerializer
from django.contrib.auth import get_user_model
from .models import CustomUser

# Create your views here.
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)

        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, method=['POST'])
    def follow_user(self, request, pk=None):
        user_to_follow = self.get_object()
        request.user.follow(user_to_follow)
        return Response({'status': f"you are now following {user_to_follow.email}"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def unfollow_user(self, request, pk=None):
        user_to_unfollow = self.get_object()
        request.user.unfollow(user_to_unfollow)
        return Response({'status': f'you have unfollowed {user_to_unfollow.email}'}, status=status.HTTP_200_OK)
