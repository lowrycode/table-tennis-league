# Generated by Django 4.2.20 on 2025-06-16 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0045_alter_fixtureresult_winner_singlesmatch_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='singlesmatch',
            options={'ordering': ['home_player', 'away_player']},
        ),
        migrations.AlterField(
            model_name='singlesmatch',
            name='away_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_singles_matches', to='league.teamplayer'),
        ),
        migrations.AlterField(
            model_name='singlesmatch',
            name='home_player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_singles_matches', to='league.teamplayer'),
        ),
    ]
