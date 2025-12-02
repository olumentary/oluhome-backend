from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import Vendor
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    VendorListSerializer,
    VendorDetailSerializer,
)

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user data in response"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the newly registered user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """User login endpoint that returns access and refresh tokens"""
    serializer_class = CustomTokenObtainPairSerializer


class RefreshTokenView(TokenRefreshView):
    """Refresh access token endpoint"""
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current authenticated user"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class VendorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing vendors.
    Provides CRUD operations (Create, Read, Update, Delete).
    Users can only see and manage their own vendors.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter vendors to only show those belonging to the current user"""
        return Vendor.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use list serializer for list view, detail serializer for detail view"""
        if self.action == 'list':
            return VendorListSerializer
        return VendorDetailSerializer
    
    def perform_create(self, serializer):
        """Automatically assign the vendor to the current user"""
        serializer.save(user=self.request.user)
