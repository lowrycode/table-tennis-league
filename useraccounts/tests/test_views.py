from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="difficulttoguess!",
        )

    def test_page_returns_correct_status_code(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        response = self.client.get(reverse("account_signup"))
        self.assertTemplateUsed(response, "account/signup.html")

    def test_page_redirects_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_signup"))
        self.assertRedirects(response, reverse("home"))

    def test_page_has_title(self):
        response = self.client.get(reverse("account_signup"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Sign Up")

    # Test invalid form submissions
    def test_invalid_form_missing_required_fields(self):
        form_data = {
            "email": "",
            "username": "",
            "password1": "",
            "password2": "",
        }

        # Check form errors are raised
        response = self.client.post(reverse("account_signup"), data=form_data)
        self.assertFormError(
            response, "form", "email", "This field is required."
        )
        self.assertFormError(
            response, "form", "username", "This field is required."
        )
        self.assertFormError(
            response, "form", "password1", "This field is required."
        )
        self.assertFormError(
            response, "form", "password2", "This field is required."
        )

    def test_invalid_form_non_unique_fields(self):
        form_data = {
            "username": "testuser",
            "email": "user@example.com",
            "password1": "difficulttoguess!",
            "password2": "difficulttoguess!",
        }

        # Check form errors are raised
        response = self.client.post(reverse("account_signup"), data=form_data)
        self.assertFormError(
            response,
            "form",
            "email",
            "A user is already registered with this email address.",
        )
        self.assertFormError(
            response,
            "form",
            "username",
            "A user with that username already exists.",
        )

    # Test valid form submission
    def test_valid_form(self):
        response = self.client.post(
            reverse("account_signup"),
            {
                "email": "second@example.com",
                "username": "seconduser",
                "password1": "complex!2PassValidation",
                "password2": "complex!2PassValidation",
            },
            follow=True,
        )
        # Check redirect
        self.assertRedirects(response, reverse("home"))

        # Check user created in database and contains correct info
        User = get_user_model()
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(username="seconduser")
        self.assertEqual(user.email, "second@example.com")

    def test_authenticated_user_cannot_create_new_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("account_signup"),
            {
                "email": "iamloggedin@example.com",
                "username": "trytomakewhileloggedin",
                "password1": "newsecurepassword!1",
                "password2": "newsecurepassword!1",
            },
            follow=True,
        )

        # Check redirect
        self.assertRedirects(response, reverse("home"))

        # Check user not created
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertFalse(
            User.objects.filter(username="trytomakewhileloggedin").exists()
        )
