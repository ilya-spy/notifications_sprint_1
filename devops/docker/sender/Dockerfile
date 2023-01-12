FROM python:3.10 AS base

LABEL maintainer="Daniil Bairachnyi"

RUN apt-get -y update && apt-get install -y apt-utils

ARG uid=1000
ARG gid=1000

ENV USER=etl
ENV GROUP=etl
ENV HOMEDIR=/home/${USER}
ENV APP_HOME=/usr/src
ENV APP_REQUIREMENTS=/usr/requirements
ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV PYTHONPATH=${APP_HOME}


RUN mkdir -p ${APP_HOME}
RUN mkdir -p ${APP_REQUIREMENTS}
WORKDIR ${APP_HOME}

# Create an unprivileged user
RUN groupadd -g $gid ${GROUP} && \
    useradd -d ${HOMEDIR} -s /bin/bash -u $uid -g $gid ${USER} && \
    mkdir ${HOMEDIR} && \
    chown -R ${USER}:${GROUP} ${HOMEDIR}

COPY --chown=${USER}:${GROUP} devops/etl/requirements ${APP_REQUIREMENTS}

USER ${USER}

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN /usr/local/bin/python -m pip install -r "${APP_REQUIREMENTS}/base.txt"

# -----------------------------------------------------------------------------
# production environment
# -----------------------------------------------------------------------------

FROM base AS production

USER root

USER ${USER}

RUN /usr/local/bin/python -m pip install -r "${APP_REQUIREMENTS}/prod.txt"

WORKDIR ${APP_HOME}

# -----------------------------------------------------------------------------
# development environment
# -----------------------------------------------------------------------------

FROM base AS develop

USER root

RUN apt-get install -y vim make curl git tree jq

USER ${USER}

RUN /usr/local/bin/python -m pip install -r "${APP_REQUIREMENTS}/dev.txt"

COPY --chown=${USER}:${GROUP} src/ ${APP_HOME}
