from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book
from .models import CustomUser


# Create your views here.
('can_view', 'Can View'),
('can_create', 'Can Create'),
('can_edit', 'Can Edit'),
('can_delete', 'Can Delete'),
]
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_list(request):
    return render(request, 'book_list.html')

@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    return render(request, 'add_book.html')

@permission_required("bookshelf.can_view", raise_exception=True)
def view_books(request):
    return render(request, 'all_books.html')

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_books(request):
    return render(request, 'delete_books.html')