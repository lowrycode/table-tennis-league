# Generated by Django 4.2.20 on 2025-05-15 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0022_clubinfo_free_taster'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubinfo',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
