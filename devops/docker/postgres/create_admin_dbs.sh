#!/bin/bash

psql << EOF
CREATE DATABASE ${MOVIES_DB};
GRANT ALL PRIVILEGES ON DATABASE ${MOVIES_DB} TO ${POSTGRES_USER};
EOF