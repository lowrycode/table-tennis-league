from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from home.models import NewsItem


class NewsItemTests(TestCase):
    """
    Unit tests for the NewsItem model to check creation, string representation,
    default values, ordering, is_active status and date field validation.
    """

    def test_can_create_news_item(self):
        """
        Verify NewsItem instance can be created, saved, and retrieved from the
        database.
        """
        item = NewsItem(title="Test", content="Test content")
        item.full_clean()
        item.save()
        self.assertEqual(item.title, "Test")
        self.assertEqual(item.content, "Test content")
        self.assertTrue(NewsItem.objects.filter(id=item.id).exists())

    def test_string_representation(self):
        """
        Verify string representation of NewsItem returns its title.
        """
        item = NewsItem(title="My sample title")
        self.assertEqual(str(item), "My sample title")

    def test_active_from_defaults_to_now(self):
        """
        Verify active_from field defaults to the current datetime.
        """
        item = NewsItem.objects.create(title="Test", content="Content")
        self.assertIsNotNone(item.active_from)

    def test_active_to_can_be_null(self):
        """
        Verify expiration date is optional (can be null and blank).
        """
        item = NewsItem.objects.create(
            title="No Expiry",
            content="This news item has no expiration date.",
        )
        self.assertIsNone(item.active_to)

    def test_newsitem_ordering(self):
        """
        Verify NewsItems are ordered by
        - active_from descending, then
        - title ascending.
        """
        now = timezone.now()
        item1 = NewsItem.objects.create(
            title="A",
            content="...",
            active_from=now - timezone.timedelta(days=1),
        )
        item2 = NewsItem.objects.create(
            title="B", content="...", active_from=now
        )
        item3 = NewsItem.objects.create(
            title="C", content="...", active_from=now
        )

        items = list(NewsItem.objects.all())
        self.assertEqual(items, [item2, item3, item1])

    def test_is_active_property_for_currently_active_items(self):
        """
        Verify is_active returns True for news items within their active date
        range, including those with no expiry date.
        """
        now = timezone.now()
        active_news = NewsItem.objects.create(
            title="Is active",
            content="Currently active news item with specified expiry date",
            active_from=now - timezone.timedelta(days=1),
            active_to=now + timezone.timedelta(days=1),
        )
        self.assertEqual(active_news.is_active, True)
        unending_news = NewsItem.objects.create(
            title="Is active indefinitely",
            content="Currently active news item without any expiry date",
            active_from=now - timezone.timedelta(days=1),
        )
        self.assertEqual(unending_news.is_active, True)

    def test_is_active_property_for_currently_inactive_items(self):
        """
        Verify is_active returns False for news items not yet active or
        expired.
        """
        now = timezone.now()
        future_news_with_expiry = NewsItem.objects.create(
            title="Is not yet active",
            content="And an end date is specified",
            active_from=now + timezone.timedelta(days=1),
            active_to=now + timezone.timedelta(days=2),
        )
        self.assertEqual(future_news_with_expiry.is_active, False)
        future_news_unending = NewsItem.objects.create(
            title="Is not yet active",
            content="and no expiry date set",
            active_from=now + timezone.timedelta(days=1),
        )
        self.assertEqual(future_news_unending.is_active, False)
        # Note: this test works without triggering a validation error because
        # although the create method saves the object to the database it does
        # not run the clean method
        expired_news = NewsItem.objects.create(
            title="Has expired",
            content="News item expired in the past",
            active_from=now - timezone.timedelta(days=2),
            active_to=now - timezone.timedelta(days=1),
        )
        self.assertEqual(expired_news.is_active, False)

    def test_active_to_datetime_being_earlier_than_active_from_datetime(self):
        """
        Verify validation fails if active_to is earlier than active_from.
        """
        now = timezone.now()
        days_before_start = NewsItem.objects.create(
            title="End date days before start date",
            content="...",
            active_from=now + timezone.timedelta(days=1),
            active_to=now - timezone.timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            days_before_start.full_clean()

        seconds_before_start = NewsItem.objects.create(
            title="End date seconds before start date",
            content="...",
            active_from=now + timezone.timedelta(seconds=1),
            active_to=now - timezone.timedelta(seconds=1),
        )
        with self.assertRaises(ValidationError):
            seconds_before_start.full_clean()

    def test_active_to_datetime_is_in_future(self):
        """
        Verify validation fails if active_to date is in the past.
        """
        now = timezone.now()
        end_in_past = NewsItem.objects.create(
            title="End date in the past",
            content="...",
            active_from=now - timezone.timedelta(days=2),
            active_to=now - timezone.timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            end_in_past.full_clean()
