{{ config(materialized = "table") }}

SELECT
    {{ dbt_utils.star(
		ref("int_pinochet__drop_nulls"),
		except = ['location_n', 'location', 'latitude', 'longitude', 'exact_coordinates', 'geometry']
	) }},
    count(location_n) AS n_locations,
    st_makeline("geometry" ORDER BY location_n ASC) AS "geometry"
FROM
    {{ ref("int_pinochet__drop_nulls") }}
GROUP BY
    {{ dbt_utils.star(
		ref("int_pinochet__drop_nulls"),
		except = ['location_n', 'location', 'latitude', 'longitude', 'exact_coordinates', 'geometry']
	) }}
