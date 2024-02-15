# Generated by Django 4.2.10 on 2024-02-11 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_event_address_alter_event_event_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="link",
        ),
        migrations.AddField(
            model_name="event",
            name="facebook",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="event",
            name="site",
            field=models.URLField(blank=True),
        ),
    ]
