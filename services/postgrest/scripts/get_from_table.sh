#!/bin/bash

# example postgrest query
POSTGIS_TABLE="t_pinochet__construct_geometries"
POSTGREST_ENDPOINT="http://localhost:3010"
QUERY_PARAMS="?limit=2"

echo "GET from $POSTGREST_ENDPOINT/$POSTGIS_TABLE$QUERY_PARAMS"
curl $POSTGREST_ENDPOINT/$POSTGIS_TABLE$QUERY_PARAMS -X GET -H "Content-Type: application/json" | jq