from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview



class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn', 'description')


admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)


class BookAuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookAuthor, BookAuthorAdmin)


class BookReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookReview, BookReviewAdmin)