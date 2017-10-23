import csv
import glob
import logging
from datetime import datetime

from chardet.universaldetector import UniversalDetector
from django.core.exceptions import ObjectDoesNotExist

from . import models

BATCH_SIZE = 1000
log = logging.getLogger(__name__)


def _get_csv_file(csv_file_identification, data_dir):
    file_pattern = f"{data_dir}/{csv_file_identification}*"
    data_file_candidates = glob.glob(file_pattern)
    assert len(data_file_candidates) == 1, file_pattern
    return data_file_candidates[0]


"""
    aangeleverde bestanden blijken niet UTF-8 te zijn, en er is niet aangegeven wat wel
    het import-proces faalde op de aanname dat de bestanden UTF-8 zijn, voor 1 van de 4
    bestanden. Om het import proces zekerder te maken gebruik ik chardet om de encoding
    van de files te detecteren
"""
def _get_encoding(filename):
    log.info(f"trying to detect file encoding of {filename}")
    detector = UniversalDetector()
    with open(filename, "rb") as test_run:
        for line in test_run.readlines():
            detector.feed(line)
            if detector.done: break
    detector.close()
    log.info(f"{filename}: {detector.result}")
    return detector.result['encoding']


# global list of pks to prevent double entries in woz_object
_unique_pks = set()


def _process_csv(csv_file_identification, data_dir, process_row_callback):
    data_file = _get_csv_file(csv_file_identification, data_dir)
    inferred_encoding = _get_encoding(data_file)

    with open(data_file, "r", encoding=inferred_encoding) as csv_file:
        rows = csv.reader(csv_file, delimiter=';', quotechar=None, quoting=csv.QUOTE_NONE)
        headers = next(rows)

        models = []
        _unique_pks.clear()
        for row in rows:
            model_data = dict(zip(headers, row))
            model = process_row_callback(model_data)
            if model:
                models.append(model)

            if len(models) == BATCH_SIZE:
                model_object = type(models[-1])
                model_object.objects.bulk_create(models, batch_size=BATCH_SIZE)
                models.clear()

        if len(models) > 0:
            type(models[-1]).objects.bulk_create(models, batch_size=BATCH_SIZE)


def _to_none_or_date(column):
    if len(column) == 0:
        return None
    if len(column) > 13:
        return datetime.strptime(column, '%d-%m-%Y %H:%M:%S').date()
    return datetime.strptime(column, '%d-%m-%Y').date()


"""
    negeer bekende voorkomens (lege kolom, kolem == '-'
"""
def _to_none_or_integer(column):
    if len(column) == 0 or column == '-':
        return None

    return int(column)


def _process_woz_object_row(row):
    """ guard against empty rows, ignoring them """
    try:
        pk = row['WOZ_objectnummer']
    except KeyError:
        return None

    if pk in _unique_pks:
        log.info(f"ignoring doublure WOZ objectnummer: {pk}")
        return None

    _unique_pks.add(pk)

    return models.WOZObject(
        woz_objectnummer=pk,
        volgnummer=row['Volgnummer'],
        begindatum_wozobject=_to_none_or_date(row['Begindatum_wozobject']),
        begindatum_voorkomen=_to_none_or_date(row['Begindatum_voorkomen']),
        status=row['Status'],
        gebruikscode=row['Gebruikscode'],
        soort_objectcode=row['Soort_objectcode'],
        code_gebouwd_ongebouwd=row['Code_gebouwd_ongebouwd'],
        monumentaanduiding=row['Monumentaanduiding'],
        kadastraal_subject_identificatie=row['Kadastraal_subject_identificatie'],
        subjecttype=row['Subjecttype'],
        subjectnaam=row['Subjectnaam'],
        aard_zakelijk_recht=row['Aard_zakelijk_recht'],
        openbare_ruimte_identificatie=row['Openbare_ruimte_identificatie'],
        naam_openbare_ruimte=row['Naam_openbare_ruimte'],
        huisnummer=row['Huisnummer'],
        huisletter=row['Huisletter'],
        huisnummer_toevoeging=row['Huisnummer_toevoeging'],
        nummeraanduidingidentificatie=row['Nummeraanduidingidentificatie'],
        locatieomschrijving=row['Locatieomschrijving'],
        verantwoordelijke_gemeente=row['Verantwoordelijke_gemeente'],
        betrokken_waterschap=row['Betrokken_waterschap'],
        buurtidentificatie=row['Buurtidentificatie'],
        volledige_code=row['Volledige_code']
    )


def _get_parent_woz_object(row, type):
    """ guard against empty rows, ignoring them """
    try:
        fk = row['WOZ_objectnummer']
    except KeyError:
        return None

    try:
        return models.WOZObject.objects.get(pk=fk)
    except ObjectDoesNotExist:
        log.info(f"ignoring {type}, not found parent WOZObject: {fk}")
        return None


def _process_woz_deelobject_row(row):
    woz_object = _get_parent_woz_object(row, 'WOZDeelObject')
    if not woz_object:
        return None

    return models.WOZDeelObject(
        woz_object=woz_object,
        volgnummer=row['Volgnummer'],
        begindatum_deelobject=_to_none_or_date(row['Begindatum_deelobject']),
        begindatum_voorkomen=_to_none_or_date(row['Begindatum_voorkomen']),
        code=row['Code'],
        status=row['Status'],
        bouwjaar=_to_none_or_integer(row['Bouwjaar']),
        bouwlaag=_to_none_or_integer(row['Bouwlaag']),
        renovatiejaar=_to_none_or_integer(row['Renovatiejaar']),
        oppervlakte=_to_none_or_integer(row['Oppervlakte'])
    )


def _process_woz_kadastraalobject_row(row):
    woz_object = _get_parent_woz_object(row, 'WOZKadastraalObject')
    if not woz_object:
        return None

    return models.WOZKadastraalObject(
        woz_object=woz_object,
        begindatum_relatie_wozobject=_to_none_or_date(row['Begindatum_relatie_wozobject']),
        begindatum_relatie_voorkomen=_to_none_or_date(row['Begindatum_relatie_voorkomen']),
        kadastraal_object_identificatie=row['Kadastraal_object_identificatie'],
        kadastrale_gemeentecode=row['Kadastrale_gemeentecode'],
        sectie=row['Sectie'],
        perceelnummer=row['Perceelnummer'],
        indexletter=row['Indexletter'],
        indexnummer=row['Indexnummer'],
        grootte=_to_none_or_integer(row['Grootte']),
        toegekende_oppervlakte=_to_none_or_integer(row['Toegekende_oppervlakte']),
        meegetaxeerde_oppervlakte=_to_none_or_integer(row['Meegetaxeerde_oppervlakte'])
    )


def _process_woz_waardebeschikking_row(row):
    woz_object = _get_parent_woz_object(row, 'WOZ_waardebeschikking')
    if not woz_object:
        return None

    return models.WOZWaardeBeschikking(
        woz_object=woz_object,
        begindatum_waarde_object=_to_none_or_date(row['Begindatum_waarde_object']),
        einddatum_waarde_object=_to_none_or_date(row['Einddatum_waarde_object']),
        begindatum_waarde_voorkomen=_to_none_or_date(row['Begindatum_waarde_voorkomen']),
        vastgestelde_waarde=row['Vastgestelde_waarde'],
        waardepeildatum=_to_none_or_date(row['Waardepeildatum']),
        begindatum_waarde=_to_none_or_date(row['Begindatum_waarde']),
        begindatum_beschikking_object=_to_none_or_date(row['Begindatum_beschikking_object']),
        einddatum_beschikking_object=_to_none_or_date(row['Einddatum_beschikking_object']),
        begindatum_beschikking_voorkomen=_to_none_or_date(row['Begindatum_beschikking_voorkomen']),
        documentnummer_beschikking=row['Documentnummer_beschikking'],
        status_beschikking=row['Status_beschikking']
    )


def import_woz_files(data_dir):
    _process_csv('WOZ_wozobject_eigenaar_', data_dir, _process_woz_object_row)
    _process_csv('WOZ_wozdeelobject_', data_dir, _process_woz_deelobject_row)
    _process_csv('WOZ_kadastraalobject_', data_dir, _process_woz_kadastraalobject_row)
    _process_csv('WOZ_waarde_beschikking_', data_dir, _process_woz_waardebeschikking_row)
