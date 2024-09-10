from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomerUserCreationForm, UserEditForm, ProfileEditForm
from .models import Post, Profile
from django.views.generic import CreateView


# Create your views here.
class RegisterView(CreateView):
    form_class = CustomerUserCreationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')


def profile_update(request, pk):
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