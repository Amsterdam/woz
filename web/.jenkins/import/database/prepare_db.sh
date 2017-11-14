#!/bin/bash

/bin/update-db.sh atlas root
psql -U atlas -c 'create table nummeraanduiding_gebruiksdoelen as select n.landelijk_id id, g.code, g.omschrijving from bag_nummeraanduiding n, bag_gebruiksdoel g where n.verblijfsobject_id = g.verblijfsobject_id;'
pg_dump  -U atlas -t nummeraanduiding_gebruiksdoelen atlas | psql -U woz -d woz
psql -U woz -d woz -c 'ALTER TABLE nummeraanduiding_gebruiksdoelen OWNER TO woz;'

echo DONE PREPARING DATABASE
