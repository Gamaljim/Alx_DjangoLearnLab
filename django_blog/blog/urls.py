from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import (RegisterView, profile_update, PostListView, PostDetailView, PostCreateView, PostUpdateView,
                    PostDeleteView, CommentCreateView, CommentUpdateView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', profile_update, name='profile'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/comment/create', CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_pk>/comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),

]
