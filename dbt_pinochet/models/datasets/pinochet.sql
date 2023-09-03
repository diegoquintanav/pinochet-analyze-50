{{ config(
    materialized = 'view',
) }}

WITH source AS (

    SELECT
        *
    FROM
        {{ ref('pinochet_raw') }}
),
renamed AS (
    SELECT
        {{ adapter.quote("individual_id") }},
        {{ adapter.quote("group_id") }},
        {{ adapter.quote("start_date_daily") }},
        {{ adapter.quote("end_date_daily") }},
        {{ adapter.quote("start_date_monthly") }},
        {{ adapter.quote("end_date_monthly") }},
        {{ adapter.quote("last_name") }},
        {{ adapter.quote("first_name") }},
        {{ adapter.quote("minor") }},
        {{ adapter.quote("age") }},
        {{ adapter.quote("male") }},
        {{ adapter.quote("occupation") }},
        {{ adapter.quote("occupation_detail") }},
        {{ adapter.quote("victim_affiliation") }},
        {{ adapter.quote("victim_affiliation_detail") }},
        {{ adapter.quote("violence") }},
        {{ adapter.quote("method") }},
        {{ adapter.quote("interrogation") }},
        {{ adapter.quote("torture") }},
        {{ adapter.quote("mistreatment") }},
        {{ adapter.quote("targeted") }},
        {{ adapter.quote("press") }},
        {{ adapter.quote("war_tribunal") }},
        {{ adapter.quote("number_previous_arrests") }},
        {{ adapter.quote("perpetrator_affiliation") }},
        {{ adapter.quote("perpetrator_affiliation_detail") }},
        {{ adapter.quote("nationality") }},
        {{ adapter.quote("place_1") }},
        {{ adapter.quote("start_location_1") }},
        {{ adapter.quote("latitude_1") }},
        {{ adapter.quote("longitude_1") }},
        {{ adapter.quote("exact_coordinates_1") }},
        {{ adapter.quote("place_2") }},
        {{ adapter.quote("location_2") }},
        {{ adapter.quote("latitude_2") }},
        {{ adapter.quote("longitude_2") }},
        {{ adapter.quote("exact_coordinates_2") }},
        {{ adapter.quote("place_3") }},
        {{ adapter.quote("end_location_3") }},
        {{ adapter.quote("latitude_3") }},
        {{ adapter.quote("longitude_3") }},
        {{ adapter.quote("exact_coordinates_3") }},
        {{ adapter.quote("place_4") }},
        {{ adapter.quote("end_location_4") }},
        {{ adapter.quote("latitude_4") }},
        {{ adapter.quote("longitude_4") }},
        {{ adapter.quote("exact_coordinates_4") }},
        {{ adapter.quote("place_5") }},
        {{ adapter.quote("end_location_5") }},
        {{ adapter.quote("latitude_5") }},
        {{ adapter.quote("longitude_5") }},
        {{ adapter.quote("exact_coordinates_5") }},
        {{ adapter.quote("place_6") }},
        {{ adapter.quote("end_location_6") }},
        {{ adapter.quote("latitude_6") }},
        {{ adapter.quote("longitude_6") }},
        {{ adapter.quote("exact_coordinates_6") }},
        {{ adapter.quote("page") }},
        {{ adapter.quote("additional_comments") }}
    FROM
        source
)
SELECT
    *
FROM
    renamed
