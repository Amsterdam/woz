FROM amsterdam/docker_python:latest
MAINTAINER datapunt.ois@amsterdam.nl

EXPOSE 8000

RUN apt-get update \
	&& apt-get install -y \
		gdal-bin \
		libgeos-dev \
		netcat \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& adduser --system datapunt \
    && mkdir -p /static \
    && chown datapunt /static

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# CI hook - see .jenkins/README.TXT
COPY .jenkins/import /.jenkins-import/
COPY .jenkins/docker-migrate.sh /app/

USER datapunt
COPY app /app/

CMD /app/docker-entrypoint.sh