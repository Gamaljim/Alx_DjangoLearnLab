from django.urls import path
from .views import list_books, LibraryDetailView , register
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('books/', list_books, name='all_books'),
    path('library/<int:pk>', LibraryDetailView.as_view(), name='library'),
    path('register', register, name='register'),
    path('login', LoginView.as_view(template_name='relationship_app/logint.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout')
]