#!/bin/bash

# example postgrest query
POSTGIS_TABLE="dm_pinochet__base"
POSTGREST_ENDPOINT="http://localhost:3000"
QUERY_PARAMS="?limit=2"

echo "GET from $POSTGREST_ENDPOINT/$POSTGIS_TABLE$QUERY_PARAMS"
curl $POSTGREST_ENDPOINT/$POSTGIS_TABLE$QUERY_PARAMS -X GET -H "Content-Type: application/json"
echo ""