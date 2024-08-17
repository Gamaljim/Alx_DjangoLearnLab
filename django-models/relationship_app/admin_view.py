def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admins.html')
