{{ config(materialize="table") }}

SELECT DISTINCT
    {{
        dbt_utils.generate_surrogate_key(
            [
                "location_id",
                "location_n",
                "place",
                "location",
                "latitude",
                "longitude",
                "exact_coordinates",
                "geometry",
            ]
        )
    }} AS pk,
    b.{{ adapter.quote("location_id") }},
    b.{{ adapter.quote("location_n") }},
    b.{{ adapter.quote("place") }},
    b.{{ adapter.quote("location") }},
    b.{{ adapter.quote("latitude") }},
    b.{{ adapter.quote("longitude") }},
    b.{{ adapter.quote("exact_coordinates") }},
    b.{{ adapter.quote("geometry") }},
    '4326' AS {{ adapter.quote("srid") }}
FROM {{ ref("stg_pinochet__base") }} AS b
ORDER BY b.{{ adapter.quote("location_id") }}
