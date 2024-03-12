from django.core.management.base import BaseCommand

from .scrape_balfolknl import scrape_balfolknl_data
from .scrape_folkbende import scrape_folkbalbende_data
from .scrape_folkdance import scrape_folkdance_data


class Command(BaseCommand):
    help = "Displays current time"

    def load_folkbalbende(self):
        print("Processing FolkBalBende")
        scrape_folkbalbende_data()

    def load_balfolknl(self):
        print("Processing Balfolk.nl")
        scrape_balfolknl_data()

    def load_folkdance(self):
        print("Processing Folkdance.page")
        scrape_folkdance_data()

    def handle(self, *args, **kwargs):
        # self.load_folkbalbende()
        self.load_balfolknl()
        self.load_folkdance()
