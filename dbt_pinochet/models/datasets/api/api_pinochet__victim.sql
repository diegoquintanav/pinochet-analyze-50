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
    {{ adapter.quote("individual_id") }} AS "victim_id",
    {{ adapter.quote("first_name") }},
    {{ adapter.quote("last_name") }},
    {{ adapter.quote("minor") }},
    {{ adapter.quote("age") }},
    {{ adapter.quote("male") }},
    {{ adapter.quote("occupation") }},
    {{ adapter.quote("occupation_detail") }},
    {{ adapter.quote("victim_affiliation") }},
    {{ adapter.quote("victim_affiliation_detail") }},
    {{ adapter.quote("nationality") }}
FROM {{ ref("stg_pinochet__base") }}
ORDER BY {{ adapter.quote("individual_id") }}
