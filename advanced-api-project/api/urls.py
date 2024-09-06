from django.urls import path
from .views import BookListView
from .views import BookDetailView
from .views import BookCreateView
from .views import BookUpdateView
from .views import BookDeleteView

urlpatterns = [
    path('books/', BookListView.as_view(), name="books-list"),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name="books-update"),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name="books-delete"),
]
