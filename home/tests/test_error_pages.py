from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomErrorPagesTests(TestCase):
    """
    Tests for custom error pages to ensure correct status codes and templates.
    """

    def test_custom_404(self):
        """
        Check that a request to a non-existent URL returns a 404 status
        and uses the custom 404.html template.
        """
        response = self.client.get("/non-existent-page/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(
            response, "The page you requested does not exist.", status_code=404
        )

    def test_custom_403(self):
        """
        Ensure logged in users without required permissions receive a 403
        response and uses the custom 403.html template.
        """
        # Create User and login
        user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="password123",
        )
        self.client.force_login(user)

        # Attempt to access page without relevant permissions
        response = self.client.get(reverse("club_admin_dashboard"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        self.assertContains(
            response,
            "Looks like you don't have permission to view this page.",
            status_code=403,
        )
