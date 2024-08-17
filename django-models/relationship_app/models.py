from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=180)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=180)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Library(models.Model):
    name = models.CharField(max_length=180)
    books = models.ManyToManyField(Book)


class Librarian(models.Model):
    name = models.CharField(max_length=180)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)


class UserProfile(models.Model):
    CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=CHOICES, default='Member')
