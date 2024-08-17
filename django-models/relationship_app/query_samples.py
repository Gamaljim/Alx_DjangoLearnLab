from .models import Author, Book,Library,Librarian


library = Library.objects.get(name=library_name)
books = library.books.all()