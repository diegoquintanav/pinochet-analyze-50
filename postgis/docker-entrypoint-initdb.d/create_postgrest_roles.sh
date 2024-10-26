#!/bin/bash
set -e

# Create roles for PostgREST
# https://postgrest.org/en/stable/tutorials/tut0.html#step-4-create-database-for-api

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	-- Create schema and roles for PostgREST
	CREATE SCHEMA api;
	CREATE ROLE web_anon NOLOGIN;
	GRANT USAGE ON SCHEMA api TO web_anon;
	GRANT SELECT ON ALL TABLES IN SCHEMA api TO web_anon;
	CREATE ROLE authenticator NOINHERIT LOGIN PASSWORD '$PGRST_AUTHENTICATOR_PASSWORD';
	GRANT web_anon to authenticator;
EOSQL
