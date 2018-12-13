from django.contrib import admin
from .models import Book,BookInstance,Author,Genre,Language


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

admin.site.register(Author)
admin.site.register(Genre)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display =('title','imprint','author','display_genre')
    inlines = [BooksInstanceInline]







