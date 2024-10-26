{{ config(
    materialized = 'view',
) }}

WITH source AS (

    SELECT *
    FROM
        {{ ref('raw_pinochet__seed') }}
),

renamed AS (
    SELECT
        nullif({{ adapter.quote("individual_id") }}::TEXT, 'NA')::INT AS {{ adapter.quote("individual_id") }},
        nullif({{ adapter.quote("group_id") }}::TEXT, 'NA')::INT AS {{ adapter.quote("group_id") }},
        nullif({{ adapter.quote("start_date_daily") }}::TEXT, 'NA')::DATE AS {{ adapter.quote("start_date_daily") }},
        nullif({{ adapter.quote("end_date_daily") }}::TEXT, 'NA')::DATE AS {{ adapter.quote("end_date_daily") }},
        nullif({{ adapter.quote("start_date_monthly") }}::TEXT, 'NA')::DATE AS {{ adapter.quote("start_date_monthly") }},
        nullif({{ adapter.quote("end_date_monthly") }}::TEXT, 'NA')::DATE AS {{ adapter.quote("end_date_monthly") }},
        nullif({{ adapter.quote("last_name") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("last_name") }},
        nullif({{ adapter.quote("first_name") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("first_name") }},
        nullif({{ adapter.quote("minor") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("minor") }},
        nullif({{ adapter.quote("age") }}::TEXT, 'NA')::NUMERIC AS {{ adapter.quote("age") }},
        nullif({{ adapter.quote("male") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("male") }},
        nullif({{ adapter.quote("occupation") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("occupation") }},
        nullif({{ adapter.quote("occupation_detail") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("occupation_detail") }},
        nullif({{ adapter.quote("victim_affiliation") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("victim_affiliation") }},
        nullif({{ adapter.quote("victim_affiliation_detail") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("victim_affiliation_detail") }},
        nullif({{ adapter.quote("violence") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("violence") }},
        nullif({{ adapter.quote("method") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("method") }},
        nullif({{ adapter.quote("interrogation") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("interrogation") }},
        nullif({{ adapter.quote("torture") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("torture") }},
        nullif({{ adapter.quote("mistreatment") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("mistreatment") }},
        nullif({{ adapter.quote("targeted") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("targeted") }},
        nullif({{ adapter.quote("press") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("press") }},
        nullif({{ adapter.quote("war_tribunal") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("war_tribunal") }},
        nullif({{ adapter.quote("number_previous_arrests") }}::TEXT, 'NA')::NUMERIC AS {{ adapter.quote("number_previous_arrests") }},
        nullif({{ adapter.quote("perpetrator_affiliation") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("perpetrator_affiliation") }},
        nullif({{ adapter.quote("perpetrator_affiliation_detail") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("perpetrator_affiliation_detail") }},
        nullif({{ adapter.quote("nationality") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("nationality") }},
        nullif({{ adapter.quote("place_1") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("place_1") }},
        nullif({{ adapter.quote("start_location_1") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("location_1") }}, -- renamed to location_1
        nullif({{ adapter.quote("latitude_1") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("latitude_1") }},
        nullif({{ adapter.quote("longitude_1") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("longitude_1") }},
        nullif({{ adapter.quote("exact_coordinates_1") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("exact_coordinates_1") }},
        nullif({{ adapter.quote("place_2") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("place_2") }},
        nullif({{ adapter.quote("location_2") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("location_2") }},
        nullif({{ adapter.quote("latitude_2") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("latitude_2") }},
        nullif({{ adapter.quote("longitude_2") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("longitude_2") }},
        nullif({{ adapter.quote("exact_coordinates_2") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("exact_coordinates_2") }},
        nullif({{ adapter.quote("place_3") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("place_3") }},
        nullif({{ adapter.quote("end_location_3") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("location_3") }},  -- renamed to location_3
        nullif({{ adapter.quote("latitude_3") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("latitude_3") }},
        nullif({{ adapter.quote("longitude_3") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("longitude_3") }},
        nullif({{ adapter.quote("exact_coordinates_3") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("exact_coordinates_3") }},
        nullif({{ adapter.quote("place_4") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("place_4") }},
        nullif({{ adapter.quote("end_location_4") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("location_4") }}, -- renamed to location_4
        nullif({{ adapter.quote("latitude_4") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("latitude_4") }},
        nullif({{ adapter.quote("longitude_4") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("longitude_4") }},
        nullif({{ adapter.quote("exact_coordinates_4") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("exact_coordinates_4") }},
        nullif({{ adapter.quote("place_5") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("place_5") }},
        nullif({{ adapter.quote("end_location_5") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("location_5") }}, -- renamed to location_5
        nullif({{ adapter.quote("latitude_5") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("latitude_5") }},
        nullif({{ adapter.quote("longitude_5") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("longitude_5") }},
        nullif({{ adapter.quote("exact_coordinates_5") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("exact_coordinates_5") }},
        nullif({{ adapter.quote("place_6") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("place_6") }},
        nullif({{ adapter.quote("end_location_6") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("location_6") }}, -- renamed to location_6
        nullif({{ adapter.quote("latitude_6") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("latitude_6") }},
        nullif({{ adapter.quote("longitude_6") }}::TEXT, 'NA')::REAL AS {{ adapter.quote("longitude_6") }},
        nullif({{ adapter.quote("exact_coordinates_6") }}::TEXT, 'NA')::BOOLEAN AS {{ adapter.quote("exact_coordinates_6") }},
        nullif({{ adapter.quote("page") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("page") }},
        nullif({{ adapter.quote("additional_comments") }}::TEXT, 'NA')::TEXT AS {{ adapter.quote("additional_comments") }}
    FROM
        source
)

SELECT *
FROM renamed
