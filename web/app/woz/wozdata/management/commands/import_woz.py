from django.core.management import BaseCommand
from django.conf import settings
from woz.objectstore import objectstore
from woz.wozdata import woz_import
from .. import prerequisites


class Command(BaseCommand):
    def handle(self, *args, **options):
        with prerequisites.table_present('nummeraanduiding_gebruiksdoelen'):
            prerequisites.fill_referentiedata()
            objectstore.fetch_woz_files()
            woz_import.import_woz_files(data_dir=settings.LOCAL_DATA_DIR)