from django.conf import settings
from django.core.management import BaseCommand

from woz.wozdata import woz_import
from woz.wozdata.management import objectstore
from .. import prerequisites


class Command(BaseCommand):
    def handle(self, *args, **options):
        prerequisites.fill_referentiedata()
        objectstore.fetch_woz_files()
        woz_import.import_woz_files(data_dir=settings.LOCAL_DATA_DIR)