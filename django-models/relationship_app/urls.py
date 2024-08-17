from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='all_books'),
    path('library/<int:pk>', LibraryDetailView.as_view(), name='library')
]