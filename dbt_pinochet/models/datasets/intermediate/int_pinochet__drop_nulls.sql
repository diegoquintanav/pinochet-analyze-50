{{ config(
    materialized = 'view',
) }}

SELECT
	{{ dbt_utils.star(from=ref("int_pinochet__unnest_locations"), except=['geometry']) }},
	geometry
FROM
	{{ ref("int_pinochet__unnest_locations") }}
WHERE
	geometry IS NOT NULL

