# Generated by Django 4.2.20 on 2025-05-10 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_enquiry_submitted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='is_actioned',
            field=models.BooleanField(default=False),
        ),
    ]
