# Generated by Django 4.2.10 on 2024-02-19 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0027_event_events_even_visible_fbff36_idx"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="folkdancepage_id",
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
