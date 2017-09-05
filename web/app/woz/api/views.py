# Python
import logging

# Packages
from rest_framework import views
from rest_framework.response import Response
from woz.wozdata import models


log = logging.getLogger(__name__)


class WaardeView(views.APIView):
    def get(self, request, *args, **kwargs):
        kadastraal_object = request.query_params['kadastraal_object']
        log.warning(f"kadastraal_object: {kadastraal_object}")
        if kadastraal_object is None:
            return Response([])

        woz_objecten = self._get_woz_woningen_from(kadastraal_object)
        log.warning(f"woz_objecten: {woz_objecten}")
        response = []
        for woz_object in woz_objecten:
            waardebeschikkingen = models.WOZWaardeBeschikking.objects.filter(
                woz_object=woz_object.woz_objectnummer
            ).extra(order_by = ['begindatum_beschikking_object']).all()
            waarden = {}
            for waardebeschikking in waardebeschikkingen:
                waarden[waardebeschikking.begindatum_waarde] = waardebeschikking.vastgestelde_waarde
            output_waarden = {key.year:value for key, value in waarden if key.year in (2014, 2015)}
            response.append({
                'woz_object': woz_object.woz_objectnummer,
                'waarden': output_waarden
            })
        return Response(response)


    def _get_woz_woningen_from(self, kadastraal_object):
        woz_objecten = []
        woz_kadastraal_objecten = models.WOZKadastraalObject.objects.filter(
            kadastraal_object_identificatie=kadastraal_object
        ).all()
        log.warning(f"woz_kadastraal_objecten: {woz_kadastraal_objecten}")

        for woz_kadastraal_object in woz_kadastraal_objecten:
            woz_object = models.WOZObject.objects.get(
                woz_objectnummer=woz_kadastraal_object.woz_object_id
            )
            log.warning(f"woz_object: {woz_object}")
            gebruiksdoelen = models.NummeraanduidingGebruiksdoel.objects.values_list(
                'code', flat=True
            ).filter(
                nummeraanduiding=woz_object.nummeraanduidingidentificatie
            )
            log.warning(f"gebruiksdoelen: {gebruiksdoelen}")
            if '1000' in gebruiksdoelen:
                woz_objecten.append(woz_object)

        return woz_objecten
