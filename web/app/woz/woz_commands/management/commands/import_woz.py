from django.core.management import BaseCommand
from woz.objectstore import objectstore


class Command(BaseCommand):
    def handle(self, *args, **options):
        objectstore.fetch_woz_files()
