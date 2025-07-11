# Generated by Django 4.2.20 on 2025-06-06 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0045_alter_venueinfo_options_alter_venueinfo_latitude_and_more'),
        ('league', '0014_player_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='current_club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='club_players', to='clubs.club'),
        ),
    ]
