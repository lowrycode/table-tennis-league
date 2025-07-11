# Generated by Django 4.2.20 on 2025-06-16 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0042_alter_fixture_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixtureResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_score', models.PositiveSmallIntegerField()),
                ('away_score', models.PositiveSmallIntegerField()),
                ('winner', models.CharField(choices=[('home', 'Home'), ('away', 'Away'), ('draw', 'Draw')], max_length=4)),
                ('status', models.CharField(choices=[('played', 'Played'), ('forfeited', 'Forfeited')], default='played', max_length=10)),
                ('fixture', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='league.fixture')),
            ],
            options={
                'ordering': ['-fixture__datetime'],
            },
        ),
    ]
