# Python
import logging

# Packages
from rest_framework import views
from rest_framework.response import Response
from woz.wozdata import models

GEBRUIKDSOEL_WONING_CODE = '1000'
RESTRICTED_YEARS = (2014, 2015)

log = logging.getLogger(__name__)


class WaardeView(views.APIView):
    """
        kadastraal_object: ASD15 S 09256 A 0002

        retourneert de WOZ waarde in RESTRICTED_YEARS indien kadastraal object bestaat in WOZ data
        en één van de gebruiksdoelen van het verblijfsobject bij de nummeraanduiding van het WOZ
        object een woning is. Als waarde geldt die, die het meest recent (conform
        begindatum_beschikking_object) is vastgesteld.
     """

    def get(self, request, *args, **kwargs):
        kadastraal_object = request.query_params['kadastraal_object']
        if kadastraal_object is None:
            return Response([])
        kadastrale_identificatie = str.split(kadastraal_object)

        response = []

        woz_objecten = self._get_woz_woningen_from(kadastrale_identificatie)
        for woz_object in woz_objecten:
            waardebeschikkingen = models.WOZWaardeBeschikking.objects.filter(
                woz_object=woz_object.woz_objectnummer
            ).extra(order_by = ['begindatum_beschikking_object']).all()
            waarden = {}
            for waardebeschikking in waardebeschikkingen:
                waarden[waardebeschikking.begindatum_waarde] = waardebeschikking.vastgestelde_waarde
            output_waarden = {key.year:value for key, value in waarden.items() if key.year in RESTRICTED_YEARS}
            response.append({
                'woz_object': woz_object.woz_objectnummer,
                'waarden': output_waarden
            })

        return Response(response)


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
            gebruiksdoelen = models.NummeraanduidingGebruiksdoel.objects.values_list(
                'code', flat=True
            ).filter(
                nummeraanduiding=woz_object.nummeraanduidingidentificatie
            )
            if GEBRUIKDSOEL_WONING_CODE in gebruiksdoelen:
                woz_objecten.append(woz_object)

        return woz_objecten
