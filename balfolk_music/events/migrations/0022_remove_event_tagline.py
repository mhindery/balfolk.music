# Generated by Django 4.2.10 on 2024-02-18 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0021_event_balfolknl_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="tagline",
        ),
    ]
