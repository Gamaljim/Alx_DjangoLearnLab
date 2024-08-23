from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book
from .models import CustomUser


# Create your views here.

@permission_required("bookshelf.can_edit")
def book_list(request):
    return render(request, 'book_list.html')
