#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER user WITH PASSWORD 'userpwd';    # pragma: allowlist secret
    CREATE DATABASE userdb;
    GRANT ALL PRIVILEGES ON DATABASE userdb TO user;
EOSQL
