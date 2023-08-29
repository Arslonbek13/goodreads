from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Arslonbek",
                "first_name": "Arslonbek",
                "last_name": "Abduqahhorov",
                "email": "abduqahhorovarslonbek@gmail.com",
                "password": "Arslonbek0413"
            }
        )

        user = CustomUser.objects.get(username="Arslonbek")

        self.assertEqual(user.first_name, "Arslonbek")
        self.assertEqual(user.last_name, "Abduqahhorov")
        self.assertEqual(user.email, "abduqahhorovarslonbek@gmail.com")
        self.assertNotEqual(user.password, "Arslonbek0413")
        self.assertTrue(user.check_password("Arslonbek0413"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.check_password("Arslonbek0413"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Arslonbek",
                "email": "abduqahhorovarslonbek@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Arslonbek",
                "first_name": "Arslonbek",
                "last_name": "Abduqahhorov",
                "email": "abduqahhorovarslonbek",
                "password": "Arslonbek0413"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        CustomUser.objects.create(username="Arslonbek", first_name="Arslonbek")
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Arslonbek",
                "first_name": "Arslonbek",
                "last_name": "Abduqahhorov",
                "email": "abduqahhorovarslonbek",
                "password": "Arslonbek0413"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="Arslonbek", first_name="Arslonbek")
        self.db_user.set_password("Arslonbek0413")
        self.db_user.save()

    def test_successful_login(self):
        response = self.client.post(
            reverse("users:login"),
            data={
                "username": "Arslonbek",
                "password": "Arslonbek0413"
            }
        )

        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_wrong_credentials(self):
        response = self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong_username",
                "password": "Arslonbek0413"
            }
        )

        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

        response = self.client.post(
            reverse("users:login"),
            data={
                "username": "Arslonbek",
                "password": "wrong_password"
            }
        )
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="Arslonbek", password="Arslonbek0413")
        response = self.client.get(reverse("users:logout"))

        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_detail(self):
        user = CustomUser.objects.create(
            username="Arslonbek", first_name="Arslonbek", last_name="Abduqahhorov", email="arslonbek@gmail.com"
        )
        user.set_password("Arslonbek0413")
        user.save()

        self.client.login(username="Arslonbek", password="Arslonbek0413")
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="Arslonbek", first_name="Arslonbek", last_name="Abduqahhorov", email="arslonbek@gmail.com"
        )
        user.set_password("Arslonbek0413")
        user.save()

        self.client.login(username="Arslonbek", password="Arslonbek0413")
        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "Arslobek12",
                "first_name": "Arslonbek",
                "last_name": "Abduqahhorov",
                "email": "abduqahhorovarslonbek@gmail.com"
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "Abduqahhorov")
        self.assertEqual(user.email, "abduqahhorovarslonbek@gmail.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:profile"))