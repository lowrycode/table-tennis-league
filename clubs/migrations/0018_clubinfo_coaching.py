# Generated by Django 4.2.20 on 2025-05-15 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0017_clubinfo_adults'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubinfo',
            name='coaching',
            field=models.BooleanField(default=False),
        ),
    ]
