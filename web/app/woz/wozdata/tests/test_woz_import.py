import os
from unittest import TestCase, skipIf
from .. import woz_import, models


@skipIf(not os.path.exists('/app/data/fixtures'),
        'Fixtures directory not found (are you running in a container?)')
class TestImport(TestCase):
    def test_import(self):
        woz_import.import_woz_files('/app/data/fixtures')
        self.assertGreater(models.WOZObject.objects.count(), 4)
        self.assertGreater(models.WOZKadastraalObject.objects.count(), 6)
        self.assertGreater(models.WOZDeelObject.objects.count(), 11)
        self.assertGreater(models.WOZWaardeBeschikking.objects.count(), 20)