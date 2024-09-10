from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import CustomerUserCreationForm
from .models import Post
from django.views.generic import CreateView


# Create your views here.
class RegisterView(CreateView):
    form_class = CustomerUserCreationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

