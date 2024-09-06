from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from .serializers import BookSerializer
from .models import Book


# Create your views here.


class BookListView(generics.ListAPIView):
    """
        Provides a read-only list of all books.
        * Only authenticated users are allowed to access this view or they will be allowed to READ it only.
        * Supports basic filtering based on title, publication year, and author.
        *Installed django-filter with pip install django-filter
        *added it in INSTALLED APPS and added the settings needed
        *imported DjangoFilterBackend
        *and added the fields i want to filter
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'publication_year', 'author']


class BookDetailView(generics.RetrieveAPIView):
    """
        Provides a read-only list of a single book.
        * Only authenticated users are allowed to access this view or they will be allowed to READ it only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
        Provides a create API point for the Book.
        * Only authenticated users are allowed to access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
        Provides a Update API point for a single Book.
        * Only authenticated users are allowed to access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
        Provides a Delete API point for the Book.
        * Only authenticated users are allowed to access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
