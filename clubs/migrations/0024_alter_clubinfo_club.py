# Generated by Django 4.2.20 on 2025-05-16 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0023_clubinfo_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubinfo',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='infos', to='clubs.club'),
        ),
    ]
