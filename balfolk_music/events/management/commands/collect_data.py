from django.core.management.base import BaseCommand
from django.utils import timezone
from .scrape_folkbende import load_data_from_folkbende, create_from_data


class Command(BaseCommand):
    help = 'Displays current time'

    def load_folkbende(self):
        folkbende_data = load_data_from_folkbende()
        create_from_data(folkbende_data)

    def handle(self, *args, **kwargs):
        self.load_folkbende()
