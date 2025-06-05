from django.db import IntegrityError
from django.test import TestCase
from test_utils.helpers import (
    helper_test_required_fields,
    helper_test_max_length,
)
from league.models import Division


class DivisionTests(TestCase):
    """
    Unit tests for the Division model to verify field behavior, validation,
    defaults, string representation and ordering.
    """

    def test_can_create_division(self):
        """Verify valid enquiry can be saved and retrieved correctly."""
        division = Division.objects.create(name="Division 1", rank=1)
        self.assertTrue(Division.objects.filter(id=division.id).exists())

    def test_string_representation(self):
        """Verify string representation returns the division name."""
        division = Division.objects.create(name="Division 1", rank=1)
        self.assertEqual(str(division), division.name)

    def test_divisions_are_ordered_by_rank(self):
        """Verify divisions are ordered from lowest to highest rank number"""
        Division.objects.create(name="A", rank=2)
        Division.objects.create(name="B", rank=1)
        Division.objects.create(name="C", rank=3)

        divisions = list(Division.objects.all())
        ranks = [d.rank for d in divisions]

        self.assertEqual(ranks, sorted(ranks))  # should be [1, 2, 3]

    # Multi-field tests
    def test_required_fields(self):
        """
        Verify that both fields are required using helper function.
        """
        required_fields = {
            "name": True,
            "rank": True,
        }

        test_object = Division()

        # Check each field
        for field, is_required in required_fields.items():
            helper_test_required_fields(self, test_object, field, is_required)

    def test_max_lengths(self):
        """
        Verify fields with max length constraints are properly enforced
        using helper function.
        """
        fields = {
            "name": 50,
        }

        # Check each field
        valid_data = {"name": "Division 1", "rank": 1}
        for field, max_length in fields.items():
            helper_test_max_length(
                self, Division, valid_data, field, max_length
            )

    # Field constraints
    def test_name_must_be_unique(self):
        """Verify division name must be unique."""
        Division.objects.create(name="Division 1", rank=1)
        with self.assertRaises(IntegrityError):
            Division.objects.create(name="Division 1", rank=2)

    def test_rank_must_be_unique(self):
        """Verify division rank must be unique."""
        Division.objects.create(name="Division 1 North", rank=1)
        with self.assertRaises(IntegrityError):
            Division.objects.create(name="Division 1 South", rank=1)
