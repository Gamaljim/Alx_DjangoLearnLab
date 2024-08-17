from django.urls import path
from .views import all_books, LibraryDetailView

urlpatterns = [
    path('books/', all_books, name='all_books'),
    path('library/<int:pk>', LibraryDetailView.as_view(), name='library')
]