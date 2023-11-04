{{ config(
    materialized = "view",
) }}

SELECT
	{{ dbt_utils.star(
        from = ref("int_pinochet__unnest_locations"),
        except = ["geometry"]
    ) }},
    {{ adapter.quote("geometry") }}
FROM
    {{ ref("int_pinochet__unnest_locations") }}
WHERE
    {{ adapter.quote("geometry") }} IS NOT null
