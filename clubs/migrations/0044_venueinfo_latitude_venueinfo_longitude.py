# Generated by Django 4.2.20 on 2025-05-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0043_clubadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='venueinfo',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='venueinfo',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
