#!/bin/sh
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
-- Setup for postgres user and database
CREATE USER postgres WITH PASSWORD 'postgres_password';
CREATE DATABASE postgresdb OWNER postgres;
GRANT ALL PRIVILEGES ON DATABASE postgresdb TO postgres;
\c postgresdb
GRANT ALL ON SCHEMA public TO postgres;
GRANT CREATE ON SCHEMA public TO postgres;

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Setup for langgraph user and database
CREATE USER langgraph_user WITH PASSWORD 'langgraph_password';
CREATE DATABASE langgraph_db OWNER langgraph_user;
GRANT ALL PRIVILEGES ON DATABASE langgraph_db TO langgraph_user;
\c langgraph_db
GRANT ALL ON SCHEMA public TO langgraph_user;
GRANT CREATE ON SCHEMA public TO langgraph_user;
EOSQL