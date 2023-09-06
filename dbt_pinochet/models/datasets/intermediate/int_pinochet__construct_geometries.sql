{{ config(
    materialized = 'view',
) }}

WITH source AS (

    SELECT
        *
    FROM
        {{ ref('int_pinochet__renamed_and_cast') }}
),
located AS (
    SELECT
        *,
		CASE
			WHEN {{ adapter.quote("location_1") }} IS NOT NULL THEN ST_SetSRID(ST_MakePoint({{ adapter.quote("longitude_1") }}, {{ adapter.quote("latitude_1") }}), 4326)::geometry(Geometry, 4326)
			ELSE NULL
		END AS geometry_1,
		CASE
			WHEN {{ adapter.quote("location_2") }} IS NOT NULL THEN ST_SetSRID(ST_MakePoint({{ adapter.quote("longitude_2") }}, {{ adapter.quote("latitude_2") }}), 4326)::geometry(Geometry, 4326)
			ELSE NULL
		END AS geometry_2,
		CASE
			WHEN {{ adapter.quote("location_3") }} IS NOT NULL THEN ST_SetSRID(ST_MakePoint({{ adapter.quote("longitude_3") }}, {{ adapter.quote("latitude_3") }}), 4326)::geometry(Geometry, 4326)
			ELSE NULL
		END AS geometry_3,
		CASE
			WHEN {{ adapter.quote("location_4") }} IS NOT NULL THEN ST_SetSRID(ST_MakePoint({{ adapter.quote("longitude_4") }}, {{ adapter.quote("latitude_4") }}), 4326)::geometry(Geometry, 4326)
			ELSE NULL
		END AS geometry_4,
		CASE
			WHEN {{ adapter.quote("location_5") }} IS NOT NULL THEN ST_SetSRID(ST_MakePoint({{ adapter.quote("longitude_5") }}, {{ adapter.quote("latitude_5") }}), 4326)::geometry(Geometry, 4326)
			ELSE NULL
		END AS geometry_5,
		CASE
			WHEN {{ adapter.quote("location_6") }} IS NOT NULL THEN ST_SetSRID(ST_MakePoint({{ adapter.quote("longitude_6") }}, {{ adapter.quote("latitude_6") }}), 4326)::geometry(Geometry, 4326)
			ELSE NULL
		END AS geometry_6
    FROM
        source
)
SELECT
    *
FROM
    located
