# Generated by Django 4.2.10 on 2024-02-11 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0007_event_image_event_lattitude_event_longitude"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="address",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="lattitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="longitude",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
