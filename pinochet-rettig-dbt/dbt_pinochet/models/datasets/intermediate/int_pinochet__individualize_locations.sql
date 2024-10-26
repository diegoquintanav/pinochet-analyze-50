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
    ours.individual_id,
    ours.group_id,
    theirs.location_id,
    ours.location_n,
    ours.group_id as event_id, -- assume one event is linked to only one victim
    {{ dbt_utils.star(
        from=ref("int_pinochet__drop_nulls"), 
        except=["individual_id", "group_id", "location_n"], 
        relation_alias="ours") }}
FROM {{ ref("int_pinochet__drop_nulls") }} AS ours
LEFT JOIN
    identified_locations AS theirs
    ON
        ours.longitude = theirs.longitude
        AND ours.latitude = theirs.latitude
        AND ours.location = theirs.location
ORDER BY
    ours.individual_id,
    ours.group_id,
    theirs.location_id,
    event_id,
    ours.location_n,
    location_id
