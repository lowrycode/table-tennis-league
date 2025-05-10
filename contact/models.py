from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(null=True, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_actioned = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
