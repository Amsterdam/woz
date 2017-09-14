import logging
import time

from django.db import connection

log = logging.getLogger(__name__)


def is_table_present(source_table_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from information_schema.tables where table_name=%s", (source_table_name,))
            return bool(cursor.rowcount)
    except Exception as e:
        log.error(e)
        return False


def fill_referentiedata(source_table_name):
    while True:
        log.warning(f"waiting for {source_table_name} table...")
        time.sleep(30)
        if is_table_present(source_table_name) is True:
            log.warning(f"done... waiting for {source_table_name} table")
            break

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
INSERT INTO wozdata_nummeraanduidinggebruiksdoel (nummeraanduiding, code, omschrijving)
    SELECT id as nummeraanduiding, code, omschrijving
    FROM %s
            """, (source_table_name))
            return bool(cursor.rowcount)
    except Exception as e:
        log.error(e)
    return False
