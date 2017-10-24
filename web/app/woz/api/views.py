# Python
import logging

# Packages
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import views
from rest_framework.response import Response
from woz.wozdata import models
from rest_framework import status

GEBRUIKDSOEL_WONING_CODE = '1000'
RESTRICTED_YEARS = (2014, 2015)

log = logging.getLogger(__name__)


class WaardeView(views.APIView):
    """
        kadastraal_object: ASD15 S 09256 A 0002

        retourneert de WOZ waarde in RESTRICTED_YEARS indien kadastraal object bestaat in WOZ data
        en één van de gebruiksdoelen van het verblijfsobject bij de nummeraanduiding van het WOZ
        object een woning is. Als waarde voor de waardepeildatum geldt die, die het meest recent
        (volgens begindatum_beschikking_object) voor die waardepeildatum is vastgesteld.
     """

    def get(self, request, *args, **kwargs):
        if 'kadastraal_object' not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        kadastraal_object = request.query_params['kadastraal_object']
        kadastrale_identificatie = kadastraal_object.split()
        if len(kadastrale_identificatie) != 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        woz_objecten = self._get_woz_woningen_from(kadastrale_identificatie)

        woz_waarden = []
        for woz_object in woz_objecten:
            waarden = self._get_latest_waarde_per_peildatum(woz_object)
            output_waarden = {
                key.year:value
                for key, value in waarden.items()
                    if key.year in RESTRICTED_YEARS
                    and key >= woz_object.begindatum_voorkomen
            }
            woz_waarden.append({
                'woz_object': woz_object.woz_objectnummer,
                'waarden': output_waarden
            })

        response = {'kadastraal_object': kadastraal_object, 'woz_waarden': woz_waarden}
        return Response(response)

    def _get_latest_waarde_per_peildatum(self, woz_object):
        waarden = {}

        # get all 'waarden' for woz_object, order them by 'begindatum_beschikking_object'
        waardebeschikkingen = models.WOZWaardeBeschikking.objects.filter(
            woz_object=woz_object.woz_objectnummer
        ).extra(order_by=['begindatum_beschikking_object']).all()

        # only keep the last 'waarde' for each 'peildatum' (ordered by 'begindatum_beschikking_object')
        for waardebeschikking in waardebeschikkingen:
            waarden[waardebeschikking.waardepeildatum] = waardebeschikking.vastgestelde_waarde

        return waarden

    def _get_woz_woningen_from(self, kadastrale_identificatie):
        woz_kadastraal_objecten = models.WOZKadastraalObject.objects.filter(
            kadastrale_gemeentecode=kadastrale_identificatie[0],
            sectie=kadastrale_identificatie[1],
            perceelnummer=kadastrale_identificatie[2],
            indexletter=kadastrale_identificatie[3],
            indexnummer=kadastrale_identificatie[4],
        ).all()

        woz_objecten = []
        for woz_kadastraal_object in woz_kadastraal_objecten:
            woz_object = models.WOZObject.objects.get(
                woz_objectnummer=woz_kadastraal_object.woz_object_id
            )
            if woz_object.status != 'GER - Actief: gereed':
                continue
            gebruiksdoelen = models.NummeraanduidingGebruiksdoel.objects.values_list(
                'code', flat=True
            ).filter(
                nummeraanduiding=woz_object.nummeraanduidingidentificatie
            )
            if GEBRUIKDSOEL_WONING_CODE in gebruiksdoelen:
                woz_objecten.append(woz_object)

        return woz_objecten
