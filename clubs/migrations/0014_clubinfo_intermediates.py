# Generated by Django 4.2.20 on 2025-05-15 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0013_clubinfo_beginners'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubinfo',
            name='intermediates',
            field=models.BooleanField(default=False),
        ),
    ]
