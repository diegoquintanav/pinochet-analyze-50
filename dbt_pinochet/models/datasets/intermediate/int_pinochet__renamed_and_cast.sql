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
        NULLIF({{ adapter.quote("individual_id") }} :: TEXT, 'NA') :: INT AS {{ adapter.quote("individual_id") }},
        NULLIF({{ adapter.quote("group_id") }} :: TEXT, 'NA') :: INT AS {{ adapter.quote("group_id") }},
        NULLIF({{ adapter.quote("start_date_daily") }} :: TEXT, 'NA') :: DATE AS {{ adapter.quote("start_date_daily") }},
        NULLIF({{ adapter.quote("end_date_daily") }} :: TEXT, 'NA') :: DATE AS {{ adapter.quote("end_date_daily") }},
        NULLIF({{ adapter.quote("start_date_monthly") }} :: TEXT, 'NA') :: DATE AS {{ adapter.quote("start_date_monthly") }},
        NULLIF({{ adapter.quote("end_date_monthly") }} :: TEXT, 'NA') :: DATE AS {{ adapter.quote("end_date_monthly") }},
        NULLIF({{ adapter.quote("last_name") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("last_name") }},
        NULLIF({{ adapter.quote("first_name") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("first_name") }},
        NULLIF({{ adapter.quote("minor") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("minor") }},
        NULLIF({{ adapter.quote("age") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("age") }},
        NULLIF({{ adapter.quote("male") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("male") }},
        NULLIF({{ adapter.quote("occupation") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("occupation") }},
        NULLIF({{ adapter.quote("occupation_detail") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("occupation_detail") }},
        NULLIF({{ adapter.quote("victim_affiliation") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("victim_affiliation") }},
        NULLIF({{ adapter.quote("victim_affiliation_detail") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("victim_affiliation_detail") }},
        NULLIF({{ adapter.quote("violence") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("violence") }},
        NULLIF({{ adapter.quote("method") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("method") }},
        NULLIF({{ adapter.quote("interrogation") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("interrogation") }},
        NULLIF({{ adapter.quote("torture") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("torture") }},
        NULLIF({{ adapter.quote("mistreatment") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("mistreatment") }},
        NULLIF({{ adapter.quote("targeted") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("targeted") }},
        NULLIF({{ adapter.quote("press") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("press") }},
        NULLIF({{ adapter.quote("war_tribunal") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("war_tribunal") }},
        NULLIF({{ adapter.quote("number_previous_arrests") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("number_previous_arrests") }},
        NULLIF({{ adapter.quote("perpetrator_affiliation") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("perpetrator_affiliation") }},
        NULLIF({{ adapter.quote("perpetrator_affiliation_detail") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("perpetrator_affiliation_detail") }},
        NULLIF({{ adapter.quote("nationality") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("nationality") }},
        NULLIF({{ adapter.quote("place_1") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("place_1") }},
        NULLIF({{ adapter.quote("start_location_1") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("location_1") }}, -- renamed to location_1
        NULLIF({{ adapter.quote("latitude_1") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("latitude_1") }},
        NULLIF({{ adapter.quote("longitude_1") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("longitude_1") }},
        NULLIF({{ adapter.quote("exact_coordinates_1") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("exact_coordinates_1") }},
        NULLIF({{ adapter.quote("place_2") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("place_2") }},
        NULLIF({{ adapter.quote("location_2") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("location_2") }},
        NULLIF({{ adapter.quote("latitude_2") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("latitude_2") }},
        NULLIF({{ adapter.quote("longitude_2") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("longitude_2") }},
        NULLIF({{ adapter.quote("exact_coordinates_2") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("exact_coordinates_2") }},
        NULLIF({{ adapter.quote("place_3") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("place_3") }},
        NULLIF({{ adapter.quote("end_location_3") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("location_3") }},  -- renamed to location_3
        NULLIF({{ adapter.quote("latitude_3") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("latitude_3") }},
        NULLIF({{ adapter.quote("longitude_3") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("longitude_3") }},
        NULLIF({{ adapter.quote("exact_coordinates_3") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("exact_coordinates_3") }},
        NULLIF({{ adapter.quote("place_4") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("place_4") }},
        NULLIF({{ adapter.quote("end_location_4") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("location_4") }}, -- renamed to location_4
        NULLIF({{ adapter.quote("latitude_4") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("latitude_4") }},
        NULLIF({{ adapter.quote("longitude_4") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("longitude_4") }},
        NULLIF({{ adapter.quote("exact_coordinates_4") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("exact_coordinates_4") }},
        NULLIF({{ adapter.quote("place_5") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("place_5") }},
        NULLIF({{ adapter.quote("end_location_5") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("location_5") }}, -- renamed to location_5
        NULLIF({{ adapter.quote("latitude_5") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("latitude_5") }},
        NULLIF({{ adapter.quote("longitude_5") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("longitude_5") }},
        NULLIF({{ adapter.quote("exact_coordinates_5") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("exact_coordinates_5") }},
        NULLIF({{ adapter.quote("place_6") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("place_6") }},
        NULLIF({{ adapter.quote("end_location_6") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("location_6") }}, -- renamed to location_6
        NULLIF({{ adapter.quote("latitude_6") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("latitude_6") }},
        NULLIF({{ adapter.quote("longitude_6") }} :: TEXT, 'NA') :: NUMERIC AS {{ adapter.quote("longitude_6") }},
        NULLIF({{ adapter.quote("exact_coordinates_6") }} :: TEXT, 'NA') :: BOOLEAN AS {{ adapter.quote("exact_coordinates_6") }},
        NULLIF({{ adapter.quote("page") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("page") }},
        NULLIF({{ adapter.quote("additional_comments") }} :: TEXT, 'NA') :: TEXT AS {{ adapter.quote("additional_comments") }}
    FROM
        source
)
SELECT
    *
FROM
    renamed