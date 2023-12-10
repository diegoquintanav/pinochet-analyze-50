{{ config(materialize="table") }}

SELECT DISTINCT
    {{ adapter.quote("location_id") }},
    {{ adapter.quote("location") }},
    {{ adapter.quote("latitude") }},
    {{ adapter.quote("longitude") }},
    {{ adapter.quote("exact_coordinates") }},
    {{ adapter.quote("geometry") }},
    4326 AS {{ adapter.quote("srid") }}
FROM {{ ref("api_pinochet__location_and_events") }}
ORDER BY {{ adapter.quote("location_id") }}
