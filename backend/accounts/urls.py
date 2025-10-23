from django.urls import path
from .views import (
    LoginView, 
    TokenRefreshView, 
    RegisterView, 
    UserDetailView, 
    UserListView, 
    LogoutView
)

urlpatterns = [
    # JWT token endpoints
    path('token/', LoginView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
]
