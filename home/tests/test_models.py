from django.test import TestCase
from django.utils import timezone
from home.models import NewsItem


class NewsItemTests(TestCase):
    def test_can_create_news_item(self):
        item = NewsItem.objects.create(title="Test", content="Test content")
        self.assertEqual(item.title, "Test")
        self.assertEqual(item.content, "Test content")

    def test_string_representation(self):
        item = NewsItem(title="My sample title")
        self.assertEqual(str(item), "My sample title")

    def test_active_from_defaults_to_now(self):
        item = NewsItem.objects.create(title="Test", content="Content")
        self.assertIsNotNone(item.active_from)

    def test_active_to_can_be_null(self):
        item = NewsItem.objects.create(
            title="No Expiry",
            content="This news item has no expiration date.",
        )
        self.assertIsNone(item.active_to)

    def test_newsitem_ordering(self):
        now = timezone.now()
        item1 = NewsItem.objects.create(
            title="A",
            content="...",
            active_from=now - timezone.timedelta(days=1)
        )
        item2 = NewsItem.objects.create(
            title="B",
            content="...",
            active_from=now
        )
        item3 = NewsItem.objects.create(
            title="C",
            content="...",
            active_from=now
        )

        items = list(NewsItem.objects.all())
        self.assertEqual(items, [item2, item3, item1])
