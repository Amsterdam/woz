import logging
import time

from django.db import connection

log = logging.getLogger(__name__)


def is_table_present():
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from information_schema.tables where table_name='nummeraanduiding_gebruiksdoelen'")
            return bool(cursor.rowcount)
    except Exception as e:
        log.error(e)
        return False


def fill_referentiedata():
    while True:
        if is_table_present() is True:
            log.warning(f"done... waiting for nummeraanduiding_gebruiksdoelen table")
            break
        log.warning(f"waiting for nummeraanduiding_gebruiksdoelen table...")
        time.sleep(30)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
INSERT INTO wozdata_nummeraanduidinggebruiksdoel (nummeraanduiding, code, omschrijving)
    SELECT id as nummeraanduiding, code, omschrijving
    FROM nummeraanduiding_gebruiksdoelen
            """)
            return bool(cursor.rowcount)
    except Exception as e:
        log.error(e)
    return False
