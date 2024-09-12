from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RegisterView, profile_update



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', profile_update, name='profile'),
]
