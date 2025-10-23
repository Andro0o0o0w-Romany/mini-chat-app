"""
Custom JWT Authentication class for Django REST Framework
"""
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model
from .jwt_utils import get_user_from_token

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for DRF
    """
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token)
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
        
        auth_parts = auth_header.split()
        
        if len(auth_parts) != 2:
            return None
        
        prefix = auth_parts[0]
        token = auth_parts[1]
        
        if prefix.lower() != self.authentication_header_prefix.lower():
            return None
        
        return self._authenticate_credentials(token)
    
    def _authenticate_credentials(self, token):
        """
        Validate token and return user
        """
        user = get_user_from_token(token)
        
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid or expired token')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User account is disabled')
        
        return (user, token)

