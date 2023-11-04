{{ config(materialized = "table") }}

SELECT *
FROM
    {{ ref("int_pinochet__individualize_locations") }}
