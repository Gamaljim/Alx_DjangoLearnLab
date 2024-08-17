from django.shortcuts import render
from .models import Book


# Create your views here.


def books(request):
    all_books = Book.objects.all()
    return render(request, 'books.html', {'all_books': all_books})
