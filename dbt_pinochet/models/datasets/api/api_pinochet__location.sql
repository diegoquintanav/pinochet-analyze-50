{{ config(materialize="table") }}

SELECT DISTINCT
    b.{{ adapter.quote("location_id") }},
    b.{{ adapter.quote("location") }},
    b.{{ adapter.quote("latitude") }},
    b.{{ adapter.quote("longitude") }},
    b.{{ adapter.quote("exact_coordinates") }},
    b.{{ adapter.quote("geometry") }},
    b.{{ adapter.quote("srid") }}
FROM {{ ref("api_pinochet__location_and_events") }} AS b
ORDER BY b.{{ adapter.quote("location_id") }}
