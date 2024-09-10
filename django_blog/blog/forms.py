from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomerUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.emaiol = self.cleaned_data['email']
        if commit:
            user.save()
        return user