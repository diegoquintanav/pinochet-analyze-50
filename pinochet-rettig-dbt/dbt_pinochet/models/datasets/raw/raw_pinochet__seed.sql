{{ config(
    materialized = "table"
) }}

SELECT
    {{ dbt_utils.star(
        from = ref('seed_pinochet')
    ) }}
FROM
    {{ ref('seed_pinochet') }}
