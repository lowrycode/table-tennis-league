from django.test import TestCase


class CustomErrorPagesTests(TestCase):
    def test_custom_404(self):
        response = self.client.get("/non-existent-page/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(
            response, "The page you requested does not exist.", status_code=404
        )
