from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomerUserCreationForm, UserEditForm, ProfileEditForm, PostCreateEditForm
from .models import Post, Profile
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


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


@login_required
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

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

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

    return render(request, 'blog/edit_profile.html', context=context)


class PostListView(ListView):
    """
        Displays a list of all the posts with a custom object name
         so its easy to loop on all posts instead of object name
         no authentication and accessible to everyone
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    """
        Displays single post with a custom object name
         no authentication and accessible to everyone
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    """
        create a Post using the PostCreateEditForm , with a template name
        and using reverse lazy to the main page upon Creating
        overriding the form_valid method to auto assign author to be the logged in user
    """
    model = Post
    form_class = PostCreateEditForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
        Update a Post using the PostCreateEditForm , with a template name
        and using reverse lazy to the main page upon updating
        only logged in users are allowed to update posts using LogginRequiredMixin,
        and every user can only update his own posts using UserPassesTestMixin by using test_func
        getting the post using self.get_objects then return True of False based if the post.author is the same as
        the logged in user
    """
    model = Post
    form_class = PostCreateEditForm
    template_name = "blog/post_update.html"
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
        Delete a Post , with a template name
        and using reverse lazy to the main page upon Deleting
        only logged in users are allowed to delete posts using LogginRequiredMixin,
        and every user can only delete his own posts using UserPassesTestMixin by using test_func
        getting the post using self.get_objects then return True of False based if the post.author is the same as
        the logged in user
    """
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
