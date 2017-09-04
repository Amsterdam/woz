FROM build.datapunt.amsterdam.nl:5000/atlas/postgres
MAINTAINER datapunt.ois@amsterdam.nl

# postgres docker runs scripts in this dir, in alphabetical order, this well be last
COPY z_entrypoint.sh /docker-entrypoint-initdb.d/z_entrypoint.sh
