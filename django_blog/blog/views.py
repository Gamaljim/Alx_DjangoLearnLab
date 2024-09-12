from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomerUserCreationForm, UserEditForm, ProfileEditForm
from .models import Post, Profile
from django.views.generic import CreateView


class RegisterView(CreateView):
    """
    A class-based view for user registration using Django's CreateView.
    Attributes:
        form_class: Specifies the form to use for creating the user.
        template_name: The path to the HTML template to use for the registration page.
        success_url: Redirect URL which is used on successful creation, here to the login page.
    """
    form_class = CustomerUserCreationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')




def profile_update(request, pk):
    """
      A view function for updating a user's profile.
      Args:
          request: The HTTP request object.
          pk (int): The primary key of the user whose profile is to be updated.
      Workflow:
      - First, checks if the logged-in user is the same as the user who is intended to be edited.
      - If the user is authenticated and the request method is POST, handle form submission.
      - If both forms are valid, save them and redirect to the user's profile page.
      - If not POST, instantiate forms with the existing user and profile data.
      Raises:
          Http404: If the logged-in user is not the same as the user whose profile is intended to be edited.
      """
    if request.user.pk != int(pk):
        raise Http404('you are not allowed to edit another profile')
    user = User.objects.get(id=pk)
    profile = user.profile

    if request.method =='POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES,instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', pk=request.user.pk)

    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request , 'blog/edit_profile.html', context=context)