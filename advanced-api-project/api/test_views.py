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

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        update_date = {'id': self.book.pk, 'title': 'Updated Test Book'}
        response = self.client.patch(self.update_url, update_date)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.book.title, 'Updated Test Book')

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        delete_date = {'id': self.book.pk}
        response = self.client.delete(self.delete_url, delete_date)
        self.assertEquals(response.status_code, 204)

    def test_book_detail_view_permissions(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
