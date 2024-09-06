from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author


# Create your tests here.

class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.author = Author.objects.create(name='Gamal')
        self.book = Book.objects.create(title='Test Book', publication_year=2020, author=self.author)
        self.create_url = reverse('books-create')
        self.detail_url = reverse('book-detail')
        self.update_url = reverse('books-update')
        self.delete_url = reverse('books-delete')

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'title': 'New Test Book', 'publication_year': 2022, 'author': self.author.pk}
        response = self.client.post(self.create_url, data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Book.objects.get(pk=response.data['id']).title, 'New Test Book')