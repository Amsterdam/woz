Datapunt WOZ API
================

Project om WOZ waarden van BAG objecten beschikbaar te maken in een API.

Voor lokaal development: start de database en download de kant en klare woz database van acceptatie:

```bash
docker-compose up -d database
docker-compose exec database update-db.sh woz
```

