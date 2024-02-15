# Generated by Django 4.2.10 on 2024-02-11 16:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Playlist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField()),
                (
                    "platform",
                    models.CharField(
                        choices=[("spotify", "Spotify"), ("soundcloud", "SoundCloud"), ("youtube", "Youtube")],
                        max_length=16,
                    ),
                ),
                ("visible", models.BooleanField(default=True)),
            ],
        ),
    ]
