#!/bin/sh
set -e

# Langgraph setup
psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
CREATE USER postgres WITH PASSWORD 'postgres_password';
CREATE DATABASE postgresdb OWNER postgres;
GRANT ALL PRIVILEGES ON DATABASE postgresdb TO postgres;
\c postgresdb
GRANT ALL ON SCHEMA public TO postgres;
GRANT CREATE ON SCHEMA public TO postgres;
EOSQL
