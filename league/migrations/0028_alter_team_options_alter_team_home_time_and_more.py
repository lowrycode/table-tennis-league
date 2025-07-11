# Generated by Django 4.2.20 on 2025-06-06 17:06

import datetime
from django.db import migrations, models
import league.validators


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0027_team_approved'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['team_name']},
        ),
        migrations.AlterField(
            model_name='team',
            name='home_time',
            field=models.TimeField(default=datetime.time(19, 0), validators=[league.validators.validate_match_time]),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('team_name', 'season'), name='team_name_and_season'),
        ),
    ]
