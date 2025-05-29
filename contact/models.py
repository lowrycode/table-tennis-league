from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Enquiry(models.Model):
    """
    Represents a single contact enquiry submitted from the Contact page.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="enquiries",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(null=True, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_actioned = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ["-submitted_at"]

    def __str__(self):
        return self.subject
