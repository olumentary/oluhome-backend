from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    RegisterView,
    LoginView,
    RefreshTokenView,
    get_current_user,
    VendorViewSet,
)

app_name = 'api'

# Router for ViewSets
router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('auth/user/', get_current_user, name='current_user'),
    
    # Legacy token endpoints (optional - can be removed if not needed)
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Include router URLs
    path('', include(router.urls)),
]

