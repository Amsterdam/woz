FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

EXPOSE 8000

RUN adduser --system datapunt \
    && mkdir -p /static \
    && chown datapunt /static \
    && mkdir -p  /app/data \
    && chown datapunt  /app/data

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# CI hook - see .jenkins/README.TXT
COPY .jenkins/import /.jenkins-import/
COPY .jenkins/docker-migrate.sh /app/

# Tests
COPY .jenkins /app/.jenkins/

# Codebase
COPY app /app/

USER datapunt

RUN export DJANGO_SETTINGS_MODULE=woz.settings
CMD uwsgi

