FROM python:3.10

RUN apt-get update && apt-get install -y netcat

ENV PYTHONUNBUFFERED=1

COPY devops/admin/requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt
COPY src/admin ./admin

WORKDIR ./admin

COPY /devops/docker/admin/docker-entrypoint.sh ./docker-entrypoint.sh

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]
