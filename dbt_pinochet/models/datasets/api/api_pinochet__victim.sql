{{ config(materialize="table") }}

SELECT DISTINCT
    {{
        dbt_utils.generate_surrogate_key(
            [
                "individual_id",
                "first_name",
                "last_name",
                "minor",
                "age",
                "male",
                "occupation",
                "occupation_detail",
                "victim_affiliation",
                "victim_affiliation_detail",
                "nationality",
            ]
        )
    }} AS pk,
    b.{{ adapter.quote("individual_id") }},
    b.{{ adapter.quote("first_name") }},
    b.{{ adapter.quote("last_name") }},
    b.{{ adapter.quote("minor") }},
    b.{{ adapter.quote("age") }},
    b.{{ adapter.quote("male") }},
    b.{{ adapter.quote("occupation") }},
    b.{{ adapter.quote("occupation_detail") }},
    b.{{ adapter.quote("victim_affiliation") }},
    b.{{ adapter.quote("victim_affiliation_detail") }},
    b.{{ adapter.quote("nationality") }}
FROM {{ ref("stg_pinochet__base") }} AS b
ORDER BY b.{{ adapter.quote("individual_id") }}
