# Python
import logging

# Packages
from rest_framework.test import APITestCase
from woz.wozdata import woz_import, models

log = logging.getLogger(__name__)


class TestWaardeView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        woz_import.import_woz_files('/app/data/fixtures')

        models.NummeraanduidingGebruiksdoel(
            nummeraanduiding='0363200000248669',
            code='1200').save()
        models.NummeraanduidingGebruiksdoel(
            nummeraanduiding='0363200000248669',
            code='1000').save()
        models.NummeraanduidingGebruiksdoel(
            nummeraanduiding='0363200000490689',
            code='1000').save()
        models.NummeraanduidingGebruiksdoel(
            nummeraanduiding='0363200000452238',
            code='1000').save()
        models.NummeraanduidingGebruiksdoel(
            nummeraanduiding='0363200000162438',
            code='1000').save()
        models.NummeraanduidingGebruiksdoel(
            nummeraanduiding='0363200000137332',
            code='1200').save()
        models.NummeraanduidingGebruiksdoel(
            nummeraanduiding='0363200000137332',
            code='1400').save()

    @classmethod
    def tearDownClass(cls):
        models.NummeraanduidingGebruiksdoel.objects.all().delete()
        models.WOZWaardeBeschikking.objects.all().delete()
        models.WOZDeelObject.objects.all().delete()
        models.WOZKadastraalObject.objects.all().delete()
        models.WOZObject.objects.all().delete()
        super().tearDownClass()

    def test_get_no_paramater(self):
        response = self.client.get('/woz/waarde/')
        self.assertEqual(response.status_code, 400)

    def test_get_wrong_paramater(self):
        response = self.client.get('/woz/waarde/?kadastraal_object=ASD15 S 09256 A')
        self.assertEqual(response.status_code, 400)

    def test_get_non_existent_kadastraal_object(self):
        response = self.client.get('/woz/waarde/?kadastraal_object=ASD15 S 09256 A 0003')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(response.data))

    def test_get_kadastraal_object1(self):
        response = self.client.get('/woz/waarde/?kadastraal_object=ASD15 S 09256 A 0002')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data))
        self.assertEqual('036398765431', response.data[0]['woz_object'])
        self.assertEqual(159000, response.data[0]['waarden'][2014])
        self.assertEqual(166000, response.data[0]['waarden'][2015])
        log.warning(f"1: {response.data}")

    def test_get_kadastraal_object2(self):
        response = self.client.get('/woz/waarde/?kadastraal_object=ASD15 S 09256 A 0093')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data))
        self.assertEqual('036398765431', response.data[0]['woz_object'])
        self.assertEqual(159000, response.data[0]['waarden'][2014])
        self.assertEqual(166000, response.data[0]['waarden'][2015])
        log.warning(f"2: {response.data}")

    def test_get_kadastraal_object_new_price(self):
        response = self.client.get('/woz/waarde/?kadastraal_object=ASD15 S 09256 A 0013')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.data))
        self.assertEqual('036398765432', response.data[0]['woz_object'])
        self.assertEqual(158000, response.data[0]['waarden'][2014])
        self.assertEqual(167000, response.data[0]['waarden'][2015])
        log.warning(f"3: {response.data}")

    def test_get_kadastraal_object_multiple_woz_objects(self):
        response = self.client.get('/woz/waarde/?kadastraal_object=ASD15 S 04638 G 0000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.data))
        self.assertEqual('036398765433', response.data[0]['woz_object'])
        self.assertEqual(293500, response.data[0]['waarden'][2014])
        self.assertEqual(294500, response.data[0]['waarden'][2015])
        self.assertEqual('036398765434', response.data[1]['woz_object'])
        self.assertEqual(283500, response.data[1]['waarden'][2014])
        self.assertEqual(285500, response.data[1]['waarden'][2015])
        log.warning(f"5: {response.data}")

    def test_get_non_woonfunctie_kadastraal_object6(self):
        response = self.client.get('/woz/waarde/?kadastraal_object=ASD15 S 04639 G 0000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(response.data))


