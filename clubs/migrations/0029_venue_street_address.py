# Generated by Django 4.2.20 on 2025-05-17 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0028_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='street_address',
            field=models.CharField(default='Street', max_length=100),
            preserve_default=False,
        ),
    ]
