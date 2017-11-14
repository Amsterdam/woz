Datapunt WOZ API
================

Project om WOZ waarden van BAG objecten beschikbaar te maken in een API.

Voor lokaal development: start de database en download de kant en klare woz database van acceptatie:

```bash
docker-compose up -d --build database
```

Wanneer de database is geinstalleerd (check bijvoorbeeld met `docker logs -f woz_database_1` de voortgang) start dan de
woz docker:

```bash
docker-compose up -d --build web
```
