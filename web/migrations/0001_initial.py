# Generated by Django 3.1 on 2020-09-08 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.PositiveIntegerField()),
                ('loses', models.PositiveIntegerField()),
                ('ties', models.PositiveIntegerField()),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ready_to_play', models.BooleanField(default=False)),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.player')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator_move', models.CharField(blank=True, choices=[('R', 'Rock'), ('P', 'Paper'), ('S', 'Scissors')], max_length=15)),
                ('opponent_move', models.CharField(blank=True, choices=[('R', 'Rock'), ('P', 'Paper'), ('S', 'Scissors')], max_length=15)),
                ('room', models.CharField(max_length=255)),
                ('completed', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='web.player')),
                ('opponent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='web.player')),
            ],
        ),
    ]
