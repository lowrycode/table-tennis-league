# Generated by Django 4.2.20 on 2025-06-05 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0007_alter_season_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_weeks', to='league.season')),
            ],
        ),
    ]
