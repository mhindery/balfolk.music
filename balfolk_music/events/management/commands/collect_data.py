from django.core.management.base import BaseCommand
from django.utils import timezone
from .scrape_folkbende import load_data_from_folkbende, create_from_data
from .scrape_balfolknl import scrape_data
from .scrape_folkdance import scrape_folkdance_data


class Command(BaseCommand):
    help = 'Displays current time'

    def load_folkbende(self):
        folkbende_data = load_data_from_folkbende()
        create_from_data(folkbende_data)

    def load_balfolknl(self):
        scrape_data()

    def load_folkdance(self):
        scrape_folkdance_data()

    def handle(self, *args, **kwargs):
        self.load_folkbende()
        # self.load_balfolknl()
