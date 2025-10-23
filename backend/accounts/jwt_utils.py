"""
Custom JWT authentication utilities using PyJWT
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_access_token(user):
    """
    Generate JWT access token for user
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    
    return token


def generate_refresh_token(user):
    """
    Generate JWT refresh token for user
    """
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    
    return token


def decode_token(token):
    """
    Decode and verify JWT token
    Returns payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_from_token(token):
    """
    Get user object from JWT token
    """
    payload = decode_token(token)
    if not payload:
        return None
    
    try:
        user = User.objects.get(id=payload.get('user_id'))
        return user
    except User.DoesNotExist:
        return None


def verify_token(token):
    """
    Verify if token is valid
    """
    payload = decode_token(token)
    return payload is not None

