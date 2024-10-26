{{ config(materialize="table") }}

WITH base AS (
    SELECT DISTINCT
        location_id,
        event_id
    FROM {{ ref("stg_pinochet__base") }}
    ORDER BY location_id, event_id
)

SELECT * FROM base
