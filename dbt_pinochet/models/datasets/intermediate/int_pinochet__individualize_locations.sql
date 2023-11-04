{{
    config(
        materialized="view",
    )
}}

WITH
unique_locations AS (

    SELECT
        t.latitude,
        t.longitude,
        t.location,
        count(*) AS count_of_events
    FROM {{ ref("int_pinochet__drop_nulls") }} AS t
    GROUP BY t.latitude, t.longitude, t.location
    ORDER BY count(*) DESC, t.latitude, t.longitude ASC, t.location ASC
),

identified_locations AS (
    SELECT
        *,
        row_number() OVER (ORDER BY count_of_events DESC) AS location_id
    FROM unique_locations
)

SELECT
    ours.*,
    theirs.location_id,
    row_number() OVER (ORDER BY ours.individual_id, ours.group_id, ours.start_date_daily, ours.end_date_daily) AS event_id
FROM {{ ref("int_pinochet__drop_nulls") }} AS ours
LEFT JOIN
    identified_locations AS theirs
    ON
        ours.longitude = theirs.longitude
        AND ours.latitude = theirs.latitude
        AND ours.location = theirs.location
