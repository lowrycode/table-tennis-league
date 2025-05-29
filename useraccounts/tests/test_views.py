from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from clubs.models import Club, ClubAdmin

User = get_user_model()


class SignUpPageTests(TestCase):
    """Tests for verifying the user registration (signup) page."""

    @classmethod
    def setUpTestData(cls):
        """Create a default user instance for use in tests."""
        cls.current_username = "testuser"
        cls.user = User.objects.create_user(
            username=cls.current_username,
            email="user@example.com",
            password="difficulttoguess!",
        )

    def test_page_returns_correct_status_code(self):
        """
        Verify that the signup page returns status code 200 for
        anonymous users.
        """
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """Verify that the signup page renders the correct HTML template."""
        response = self.client.get(reverse("account_signup"))
        self.assertTemplateUsed(response, "account/signup.html")

    def test_page_redirects_authenticated_user(self):
        """
        Verify authenticated user is redirected away from the signup page.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_signup"))
        self.assertRedirects(response, reverse("home"))

    def test_page_contains_expected_title(self):
        """Verify signup page contains the expected title."""
        response = self.client.get(reverse("account_signup"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Sign Up")

    def test_page_contains_csrf(self):
        """Verify that the signup form includes the CSRF token."""
        response = self.client.get(reverse("account_signup"))
        self.assertContains(response, "csrfmiddlewaretoken")

    # Test invalid form submissions
    def test_invalid_form_missing_required_fields(self):
        """Verify form validation when required fields are left blank."""
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
        """Verify signup fails if username or email is already in use."""
        form_data = {
            "username": self.current_username,
            "email": "user@example.com",
            "password1": "anythingwilldo!",
            "password2": "anythingwilldo!",
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
        """
        Verify user can successfully sign up with valid and unique credentials.
        """
        response = self.client.post(
            reverse("account_signup"),
            {
                "email": "second@example.com",
                "username": "seconduser",
                "password1": "complex!2PassValidation",
                "password2": "complex!2PassValidation",
            },
        )
        # Check redirect
        self.assertRedirects(response, reverse("home"))

        # Check user created in database and contains correct info
        User = get_user_model()
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(username="seconduser")
        self.assertEqual(user.email, "second@example.com")

    def test_authenticated_user_cannot_create_new_user(self):
        """Verify that an authenticated user cannot register a new account."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("account_signup"),
            {
                "email": "iamloggedin@example.com",
                "username": "trytomakewhileloggedin",
                "password1": "newsecurepassword!1",
                "password2": "newsecurepassword!1",
            },
        )

        # Check redirect
        self.assertRedirects(response, reverse("home"))

        # Check user not created
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertFalse(
            User.objects.filter(username="trytomakewhileloggedin").exists()
        )


class LoginPageTests(TestCase):
    """
    Tests for verifying the login page functionality and authentication flow.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a valid user instance used to test login behaviours.
        """
        cls.current_username = "testuser"
        cls.current_password = "difficulttoguess!"
        cls.user = User.objects.create_user(
            username=cls.current_username,
            email="user@example.com",
            password=cls.current_password,
        )

    def test_page_returns_correct_status_code(self):
        """Verify login page returns a 200 status code for anonymous users."""
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """Verify login page renders the correct HTML template."""
        response = self.client.get(reverse("account_login"))
        self.assertTemplateUsed(response, "account/login.html")

    def test_page_redirects_authenticated_user(self):
        """
        Verify that an authenticated user is redirected from the login page.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_login"))
        self.assertRedirects(response, reverse("home"))

    def test_page_contains_expected_title(self):
        """Verify login page contains the expected title content."""
        response = self.client.get(reverse("account_login"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Log in")

    def test_page_contains_csrf(self):
        """Verify login form includes CSRF token."""
        response = self.client.get(reverse("account_login"))
        self.assertContains(response, "csrfmiddlewaretoken")

    # Test invalid form submissions
    def test_invalid_form_missing_required_fields(self):
        """
        Verify form validation when login and password fields are left blank.
        """
        form_data = {"login": "", "password": ""}

        # Check form errors are raised
        response = self.client.post(reverse("account_login"), data=form_data)
        self.assertFormError(
            response, "form", "login", "This field is required."
        )
        self.assertFormError(
            response, "form", "password", "This field is required."
        )

    def test_invalid_form_incorrect_password(self):
        """Verify error message when an incorrect password is provided."""
        form_data = {
            "login": self.current_username,
            "password": "notmypassword!",
        }

        # Check form errors are raised
        response = self.client.post(reverse("account_login"), data=form_data)
        self.assertFormError(
            response,
            "form",
            None,
            ["The username and/or password you specified are not correct."],
        )

    def test_password_case_sensitive(self):
        """Verify password field is case-sensitive during login."""
        form_data = {
            "login": self.current_username,
            "password": self.current_password.upper(),
        }

        # Check form errors are raised
        response = self.client.post(reverse("account_login"), data=form_data)
        self.assertFormError(
            response,
            "form",
            None,
            ["The username and/or password you specified are not correct."],
        )

    def test_invalid_form_incorrect_username(self):
        """Verify error message when an unknown username is used."""
        form_data = {
            "login": "notaknownuser",
            "password": "wonthaveappasword!",
        }

        # Check form errors are raised
        response = self.client.post(reverse("account_login"), data=form_data)
        self.assertFormError(
            response,
            "form",
            None,
            ["The username and/or password you specified are not correct."],
        )

    # Test valid form submission
    def test_valid_form(self):
        """
        Verify successful login with correct credentials and presence of
        success message.
        """
        ...
        form_data = {
            "login": self.current_username,
            "password": self.current_password,
        }
        response = self.client.post(
            reverse("account_login"),
            data=form_data,
        )
        # Check redirect
        self.assertRedirects(response, reverse("home"))

        # Check user is logged in
        user = response.context["user"]
        self.assertTrue(user.is_authenticated)

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Successfully signed in as testuser.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

    def test_authenticated_user_cannot_log_in(self):
        """
        Verify that an already authenticated user cannot log in as a
        different user.
        """
        # Create second user for login attempt
        user2 = User.objects.create_user(
            username="seconduser",
            email="user2@example.com",
            password="alsodifficulttotguess!",
        )
        form_data = {
            "login": "seconduser",
            "password": "alsodifficulttotguess!",
        }

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("account_login"),
            form_data,
            follow=True,
        )

        # Check redirect
        self.assertRedirects(response, reverse("home"))

        # Check user still logged in as original user
        user = response.context["user"]
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, self.user.username)
        self.assertNotEqual(user.username, user2.username)


class LogoutPageTests(TestCase):
    """
    Tests for verifying the logout functionality.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a valid user instance for testing logout behaviour.
        """
        cls.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="difficulttoguess!",
        )

    def test_page_returns_correct_status_code(self):
        """
        Verify logout page returns a 200 status code when accessed by an
        authenticated user.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """Verify logout page uses the correct HTML template."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_logout"))
        self.assertTemplateUsed(response, "account/logout.html")

    def test_page_redirects_unauthenticated_user(self):
        """
        Verify that unauthenticated users are redirected away from the
        logout page.
        """
        response = self.client.get(reverse("account_logout"))
        self.assertRedirects(response, reverse("home"))

    def test_page_contains_expected_title(self):
        """Verify logout page contains the expected title content."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_logout"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Log Out")

    def test_page_contains_csrf(self):
        """Verify logout form includes the CSRF token."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_logout"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_page_contains_go_back_button(self):
        """
        Verify that the logout page contains a 'Go Back' button with correct
        behaviour.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_logout"))
        self.assertContains(response, "<a")
        self.assertContains(response, "href")
        self.assertContains(response, "Go Back")
        self.assertContains(response, "javascript:history.back()")

    def test_user_can_logout(self):
        """
        Verify that a user can successfully log out and is shown a
        confirmation message.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse("account_logout"), follow=True)

        # Check logged out
        user = response.context["user"]
        self.assertFalse(user.is_authenticated)

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "You have signed out.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

        # Check redirect
        self.assertRedirects(response, reverse("home"))


class ChangePasswordPageTests(TestCase):
    """
    Tests for verifying the password change functionality.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a valid user instance for testing password change behaviour.
        """
        cls.current_password = "difficulttoguess!"
        cls.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password=cls.current_password,
        )

    def test_page_returns_correct_status_code(self):
        """
        Verify password change page returns a 200 status code when accessed by
        an authenticated user.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_change_password"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """Verify password change page renders the correct template."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_change_password"))
        self.assertTemplateUsed(response, "account/password_change.html")

    def test_page_redirects_unauthenticated_user(self):
        """
        Verify that unauthenticated users are redirected to the login page
        when attempting to access password change.
        """
        response = self.client.get(reverse("account_change_password"))
        self.assertRedirects(
            response,
            (
                f"{reverse("account_login")}"
                f"?next={reverse("account_change_password")}"
            ),
        )

    def test_page_contains_expected_title(self):
        """Verify password change page displays the expected title."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_change_password"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Change Password")

    def test_page_contains_csrf(self):
        """Verify form includes the CSRF token."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_change_password"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_page_contains_go_back_button(self):
        """
        Verify that the password change page contains a 'Go Back' button
        linking to the account settings page.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_change_password"))
        self.assertContains(response, "<a")
        self.assertContains(response, f'href="{reverse("account_settings")}"')
        self.assertContains(response, "Go Back")

    def test_invalid_form_missing_required_fields(self):
        """
        Verify validation errors are raised when required fields are left
        blank in the form.
        """
        form_data = {
            "oldpassword": "",
            "password1": "",
            "password2": "",
        }

        self.client.force_login(self.user)

        # Check form errors are raised
        response = self.client.post(
            reverse("account_change_password"), data=form_data
        )
        self.assertFormError(
            response, "form", "oldpassword", "This field is required."
        )
        self.assertFormError(
            response, "form", "password1", "This field is required."
        )
        self.assertFormError(
            response, "form", "password2", "This field is required."
        )

    def test_invalid_form_incorrect_old_password(self):
        """Verify error is shown when the current password is incorrect."""
        form_data = {
            "oldpassword": "notmyoldpassword!",
            "password1": "anewandbetterpassword!",
            "password2": "anewandbetterpassword!",
        }

        self.client.force_login(self.user)

        # Check form errors are raised
        response = self.client.post(
            reverse("account_change_password"), data=form_data
        )
        self.assertFormError(
            response,
            "form",
            "oldpassword",
            "Please type your current password.",
        )

    def test_invalid_form_non_matching_passwords(self):
        """Verify validation fails when the new passwords do not match."""
        form_data = {
            "oldpassword": self.current_password,
            "password1": "anewandbetterpassword!",
            "password2": "shouldbethesamepassword!",
        }

        self.client.force_login(self.user)

        # Check form errors are raised
        response = self.client.post(
            reverse("account_change_password"), data=form_data
        )
        self.assertFormError(
            response,
            "form",
            "password2",
            "You must type the same password each time.",
        )

    def test_invalid_form_passwords_case_sensitive(self):
        """
        Verify that mismatched password casing results in a validation error.
        """
        form_data = {
            "oldpassword": self.current_password,
            "password1": "anewandbetterpassword!",
            "password2": "aNewAndBetTerPasSword!",
        }

        self.client.force_login(self.user)

        # Check form errors are raised
        response = self.client.post(
            reverse("account_change_password"), data=form_data
        )
        self.assertFormError(
            response,
            "form",
            "password2",
            "You must type the same password each time.",
        )

    def test_user_can_change_password(self):
        """
        Verify that a user can successfully change their password and is
        redirected with a success message.
        """
        form_data = {
            "oldpassword": self.current_password,
            "password1": "anewandbetterpassword!",
            "password2": "anewandbetterpassword!",
        }

        self.client.force_login(self.user)
        response = self.client.post(
            f"{reverse("account_change_password")}?next={reverse("contact")}",
            data=form_data,
            follow=True,
        )

        # Check password has been updated
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(self.current_password))
        self.assertTrue(self.user.check_password("anewandbetterpassword!"))

        # Check redirect
        self.assertRedirects(response, reverse("contact"))

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Password successfully changed.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)


class AccountSettingsPageTests(TestCase):
    """Tests for Account Settings page."""

    @classmethod
    def setUpTestData(cls):
        """Create a test user ready for use in tests."""
        cls.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="difficulttoguess!",
        )

    def test_page_returns_correct_status_code(self):
        """
        Verify that the account settings page returns a 200 status code
        for authenticated users.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """Verify that the account settings page uses the correct template."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))
        self.assertTemplateUsed(response, "useraccounts/account_settings.html")

    def test_page_redirects_unauthenticated_user(self):
        """
        Verify unauthenticated users are redirected to login with next
        parameter.
        """
        response = self.client.get(reverse("account_settings"))
        self.assertRedirects(
            response,
            f"{reverse("account_login")}?next={reverse("account_settings")}",
        )

    def test_page_contains_expected_title(self):
        """
        Verify account settings page contains the expected title.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Account Settings")

    def test_page_has_email_address_section(self):
        """
        Verify account settings page shows the user's email and a change link.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))
        self.assertContains(response, 'id="user-email"')
        self.assertContains(response, self.user.email)
        self.assertContains(response, "Change</a>")

    def test_page_has_password_section(self):
        """Verify account settings page includes a password section."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))
        self.assertContains(response, "Password</h2>")

    def test_page_has_club_admin_section_if_user_has_club_admin_status(self):
        """
        Verify club admin section appears if the user has club admin status.
        """
        # Create Club and Club Admin
        club = Club.objects.create(name="Test Club")
        club_admin = ClubAdmin.objects.create(user=self.user, club=club)

        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))

        self.assertContains(response, "Club Admin</h2>")
        self.assertContains(response, club_admin.club.name)

    def test_page_has_no_club_admin_section_if_no_club_admin_status(self):
        """
        Verify club admin section does not appear if the user is not a
        club admin.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))
        self.assertNotContains(response, "Club Admin</h2>")

    def test_page_has_delete_account_section(self):
        """
        Verify account settings page contains the delete account section.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("account_settings"))
        self.assertContains(response, "Delete Account")
        self.assertContains(response, "WARNING: This action cannot be undone.")


class ChangeEmailPageTests(TestCase):
    """Tests for Change Email page."""

    @classmethod
    def setUpTestData(cls):
        """Create user for use in tests"""
        cls.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="difficulttoguess!",
        )

    def test_page_returns_correct_status_code(self):
        """
        Verify page returns a 200 status code for authenticated users.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("change_email"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """Verify page uses the correct template."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("change_email"))
        self.assertTemplateUsed(response, "useraccounts/change_email.html")

    def test_page_redirects_unauthenticated_user(self):
        """
        Verify unauthenticated users are redirected to login page with
        next parameter when accessing change email page.
        """
        response = self.client.get(reverse("change_email"))
        self.assertRedirects(
            response,
            f"{reverse("account_login")}?next={reverse("change_email")}",
        )

    def test_page_contains_expected_title(self):
        """
        Verify the change email page contains the expected title.
        """
        self.client.force_login(self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse("change_email"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Change Email")

    def test_page_contains_csrf(self):
        """Verify the change email page contains the CSRF token."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("change_email"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_page_contains_go_back_button(self):
        """
        Verify change email page contains a go back button linking to
        account settings.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("change_email"))
        self.assertContains(response, "<a")
        self.assertContains(response, f'href="{reverse("account_settings")}"')
        self.assertContains(response, "Go Back")

    def test_user_can_update_email(self):
        """
        Verify authenticated user can successfully update their email address.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("change_email"),
            {"email": "myupdatedemail@example.com"},
            follow=True,
        )

        # Check email has been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "myupdatedemail@example.com")

        # Check redirect
        self.assertRedirects(response, reverse("account_settings"))

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Your email has been updated.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

    def test_invalid_email_does_not_update_user(self):
        """
        Verify that submitting an invalid email does not update the user's
        email and raises form errors.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("change_email"),
            {"email": "not_an_email"},
        )

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, "not_an_email")
        self.assertEqual(self.user.email, "user@example.com")
        self.assertFormError(
            response, "form", "email", "Enter a valid email address."
        )


class ConfirmAccountDeletePageTests(TestCase):
    """
    Tests for the account deletion confirmation page.
    """

    def setUp(self):
        """Create user for testing account deletion."""
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="difficulttoguess!",
        )

    def test_page_returns_correct_status_code(self):
        """
        Verify that the account deletion page returns status code 200
        for an authenticated user.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_account"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """
        Verify correct template is used for account deletion confirmation page.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_account"))
        self.assertTemplateUsed(
            response, "useraccounts/confirm_account_delete.html"
        )

    def test_page_redirects_unauthenticated_user(self):
        """
        Verify that unauthenticated users are redirected to the login page.
        """
        response = self.client.get(reverse("delete_account"))
        self.assertRedirects(
            response,
            f"{reverse("account_login")}?next={reverse("delete_account")}",
        )

    def test_page_contains_expected_title_and_warnings(self):
        """
        Verify page contains the correct title and account deletion warnings.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_account"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Delete Account?</h1>")
        self.assertContains(
            response,
            (
                "This will permanently delete your login credentials "
                "for this website."
            ),
        )
        self.assertContains(response, "action cannot be undone")

    def test_page_contains_csrf(self):
        """
        Verify that the CSRF token is present in the form.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_account"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_page_contains_cancel_button(self):
        """
        Verify cancel button linking back to the settings page is present.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_account"))
        self.assertContains(response, "<a")
        self.assertContains(response, f'href="{reverse("account_settings")}"')
        self.assertContains(response, "Cancel")

    def test_page_contains_confirm_delete_checkbox(self):
        """
        Verify that a checkbox for confirming account deletion is present.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_account"))
        self.assertContains(response, "input")
        self.assertContains(response, 'type="checkbox"')
        self.assertContains(response, 'id="confirm-account-delete"')

    def test_view_requires_confirm_delete_checkbox(self):
        """
        Verify that submitting the form without checking the confirmation box
        does not delete the account.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse("delete_account"), {})

        # Check user still exists
        self.assertTrue(
            User.objects.filter(username=self.user.username).exists()
        )

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "You must confirm before deleting your account.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.WARNING)

    def test_user_can_delete_account(self):
        """
        Verify that a user can delete their account by checking the
        confirmation box and submitting.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("delete_account"),
            {"confirm_action": "on"},
            follow=True,
        )

        # Check user is no longer in database
        self.assertFalse(
            User.objects.filter(username=self.user.username).exists()
        )

        # Check redirect
        self.assertRedirects(response, reverse("home"))

        # Check if the message is in the message queue
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Your account has been deleted.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)


class ConfirmDropClubAdminStatusPageTests(TestCase):
    """
    Tests for dropping club admin status.
    """

    def setUp(self):
        """
        Create test users and club admin relationships for test scenarios.
        """
        # Create Users
        self.user_with_admin = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="difficulttoguess!",
        )
        self.user_without_admin = User.objects.create_user(
            username="regularuser",
            email="user@example.com",
            password="difficulttoguess!",
        )

        # Create Club
        self.club = Club.objects.create(name="Test Club")

        # Create ClubAdmin for user_with_admin
        ClubAdmin.objects.create(user=self.user_with_admin, club=self.club)

    def test_page_returns_correct_status_code(self):
        """
        Verify drop club admin status page returns status code 200
        for users with club admin status.
        """
        self.client.force_login(self.user_with_admin)
        response = self.client.get(reverse("drop_club_admin_status"))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_correct_template(self):
        """
        Verify correct template is used for the drop club admin status page.
        """
        self.client.force_login(self.user_with_admin)
        response = self.client.get(reverse("drop_club_admin_status"))
        self.assertTemplateUsed(
            response, "useraccounts/confirm_drop_club_admin_status.html"
        )

    def test_page_redirects_unauthenticated_user(self):
        """
        Verify that unauthenticated users are redirected to the login page.
        """
        response = self.client.get(reverse("drop_club_admin_status"))
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next="
            f"{reverse('drop_club_admin_status')}",
        )

    def test_page_contains_expected_content(self):
        """
        Verify page includes the correct heading and content.
        """
        self.client.force_login(self.user_with_admin)
        response = self.client.get(reverse("drop_club_admin_status"))
        self.assertContains(response, "<h1")
        self.assertContains(response, "Drop Club Admin Status?")
        self.assertContains(
            response, "The club itself will not be deleted.", status_code=200
        )

    def test_post_without_confirm_delete_shows_warning(self):
        """
        Verify that submitting the form without confirming does not remove
        admin status and shows a warning.
        """
        self.client.force_login(self.user_with_admin)
        response = self.client.post(reverse("drop_club_admin_status"), {})

        # User's ClubAdmin should still exist
        self.assertTrue(
            ClubAdmin.objects.filter(user=self.user_with_admin).exists()
        )

        # Check warning message
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "You must confirm before dropping your club admin status.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.WARNING)

    def test_post_with_confirm_delete_deletes_club_admin_and_redirects(self):
        """
        Verify that submitting the form with confirmation deletes the
        user's club admin status and redirects correctly.
        """
        self.client.force_login(self.user_with_admin)
        response = self.client.post(
            reverse("drop_club_admin_status"),
            {"confirm_action": "on"},
            follow=True,
        )
        # ClubAdmin should be deleted
        self.assertFalse(
            ClubAdmin.objects.filter(user=self.user_with_admin).exists()
        )

        # Redirects to account_settings
        self.assertRedirects(response, reverse("account_settings"))

        # Success message
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "Your account no longer has club admin status.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.SUCCESS)

    def test_post_with_confirm_delete_for_user_without_club_admin(self):
        """
        Verify that a user without club admin status receives a warning when
        attempting to drop it.
        """
        self.client.force_login(self.user_without_admin)
        response = self.client.post(
            reverse("drop_club_admin_status"),
            {"confirm_action": "on"},
            follow=True,
        )
        # Confirm no ClubAdmin exists
        self.assertFalse(
            ClubAdmin.objects.filter(user=self.user_without_admin).exists()
        )

        # Redirects to account_settings
        self.assertRedirects(response, reverse("account_settings"))

        # Warning message about no club admin status
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertIn(
            "You do not currently have club admin status.",
            msgs[0].message,
        )
        self.assertEqual(msgs[0].level, messages.WARNING)
