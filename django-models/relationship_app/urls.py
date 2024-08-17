from django.urls import path
from . import views
from . import librarian_view
from . import member_view
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('books/', views.list_books, name='all_books'),
    path('library/<int:pk>', views.LibraryDetailView.as_view(), name='library'),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='relationship_app/logint.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admins', views.admin_view, name='admins'),
    path('librarians', librarian_view.librarian_view, name='librarians'),
    path('members', member_view.member_view, name='members'),
    path('add_book/', views.can_add_book),
    path('edit_book/', views.can_change_book),
    path('delete_book/', views.can_delete_book),
]