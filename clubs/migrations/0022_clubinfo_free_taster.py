# Generated by Django 4.2.20 on 2025-05-15 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0021_clubinfo_membership_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubinfo',
            name='free_taster',
            field=models.BooleanField(default=False),
        ),
    ]
