# Generated by Django 4.2.20 on 2025-06-06 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0012_player_week_unique_season_and_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='surname',
            field=models.CharField(default='John', max_length=50),
            preserve_default=False,
        ),
    ]
