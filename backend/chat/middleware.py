from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from accounts.jwt_utils import get_user_from_token

User = get_user_model()


@database_sync_to_async
def get_user_from_token_async(token_key):
    """Get user from JWT token asynchronously"""
    user = get_user_from_token(token_key)
    return user if user else AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """Custom middleware to authenticate WebSocket connections using JWT"""
    
    async def __call__(self, scope, receive, send):
        # Get token from query string
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]
        
        if token:
            scope['user'] = await get_user_from_token_async(token)
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
