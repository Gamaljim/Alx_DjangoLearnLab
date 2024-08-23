from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Book
from .models import CustomUser


# Register your models here.
class CustomerUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ('date_of_birth', 'profile_photo'),
                }),
    )


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')
    list_filter = ('title', 'author')


admin.site.register(Book, BookAdmin)
