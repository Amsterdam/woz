FROM build.datapunt.amsterdam.nl:5000/atlas/postgres
MAINTAINER datapunt.ois@amsterdam.nl

# make prepare db script available in postgres docker
COPY prepare_db.sh /bin/prepare_db.sh

# postgres docker runs scripts in this dir, in alphabetical order, this well be last
COPY z_entrypoint.sh /docker-entrypoint-initdb.d/z_entrypoint.sh
