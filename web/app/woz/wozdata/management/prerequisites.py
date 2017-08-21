import logging
import time

from django.db import connection

log = logging.getLogger(__name__)


class WaitForFilledTable(object):
    def __init__(self, tablename):
        self.tablename = tablename

    def __enter__(self, tablename):
        while True:
            log.warning(f"waiting for {self.tablename} table...")
            time.sleep(10)
            if self.is_table_present is True:
                log.warning(f"done... waiting for {self.tablename} table")
                break

    def __exit__(self, key, value, traceback):
        pass

    @property
    def is_table_present(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from information_schema.tables where table_name=%s", (self.tablename,))
                return bool(cursor.rowcount)
        except Exception as e:
            log.error(e)
        return False


def table_present(tablename):
    return WaitForFilledTable(tablename)


def fill_referentiedata():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
INSERT INTO wozdata_nummeraanduidinggebruiksdoel (nummeraanduiding, code, omschrijving)
    SELECT id as nummeraanduiding, code, omschrijving
    FROM nummeraanduiding_gebruiksdoelen
    WHERE code like '10%';
            """)
            return bool(cursor.rowcount)
    except Exception as e:
        log.error(e)
    return False
