from .models import Author, Book,Library,Librarian


all_books = Book.objects.filter(author=author)