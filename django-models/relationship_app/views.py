from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic import DetailView


# Create your views here.


def all_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
