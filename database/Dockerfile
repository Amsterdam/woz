FROM amsterdam/postgres
MAINTAINER datapunt@amsterdam.nl

# postgres docker runs scripts in this dir, in alphabetical order, this well be last
COPY z_entrypoint.sh /docker-entrypoint-initdb.d/z_entrypoint.sh
