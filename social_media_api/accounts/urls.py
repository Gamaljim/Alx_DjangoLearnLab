from django.urls import path, include
from .views import LoginView, RegisterView, ProfileView, CustomUserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls))
]
