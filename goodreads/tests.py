from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):

    def test_paginated_list(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")

        user = CustomUser.objects.create(
            username="Arslonbek", first_name="Arslonbek", last_name="Abduqahhorov", email="abduqahhorovarslonbek@gmail.com"
        )

        user.set_password("Arslonbek0413")
        user.save()

        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Nice book")

        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Nice book")

        response = self.client.get(reverse("home_page") + "?page_size=2")


        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
