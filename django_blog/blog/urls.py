from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RegisterView, profile_update, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', profile_update, name='profile'),
    path('posts', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
]
