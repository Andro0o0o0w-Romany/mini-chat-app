from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer
from .jwt_utils import generate_access_token, generate_refresh_token, decode_token, get_user_from_token

User = get_user_model()


class LoginView(APIView):
    """User login endpoint"""
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        
        return Response({
            'access': access_token,
            'refresh': refresh_token,
            'user': UserSerializer(user).data
        })


class TokenRefreshView(APIView):
    """Refresh access token using refresh token"""
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Decode and verify refresh token
        payload = decode_token(refresh_token)
        
        if not payload:
            return Response(
                {'error': 'Invalid or expired refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verify it's a refresh token
        if payload.get('type') != 'refresh':
            return Response(
                {'error': 'Invalid token type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user and generate new tokens
        try:
            user = User.objects.get(id=payload.get('user_id'))
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generate new tokens
        new_access_token = generate_access_token(user)
        new_refresh_token = generate_refresh_token(user)
        
        return Response({
            'access': new_access_token,
            'refresh': new_refresh_token
        })


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': refresh_token,
                'access': access_token,
            }
        }, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """Get and update current user details"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return UserUpdateSerializer
        return UserSerializer


class UserListView(generics.ListAPIView):
    """List all users for creating conversations"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Exclude current user from the list
        return User.objects.exclude(id=self.request.user.id)


class LogoutView(APIView):
    """Logout user"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # With stateless JWT, we just return success
        # Client should remove tokens from storage
        # For token blacklisting, you'd need to implement a blacklist model
        return Response(
            {"message": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
