from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


# Create your  here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        post = super().get_object()

        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if post.author != self.request.user:
                raise PermissionDenied("You Do not have permission to modify this post")
        return post


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        comment = super().get_object()

        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if comment.author != self.request.user:
                raise PermissionDenied('You do not have permission to modify this comment')
        return comment
