from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author
# Create your tests here.

class UnitListTestCase(APITestCase):
    def setUp(self):
