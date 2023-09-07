{{ config(materialized = "table") }}

SELECT
    {{ dbt_utils.star(
		ref("int_pinochet__drop_nulls"),
		except = ['location_n', 'location', 'latitude', 'longitude', 'exact_coordinates', 'geometry']
	)}},
	count(dm.location_n) as n_locations,
    st_makeline(dm.geometry ORDER BY dm.location_n ASC) AS geometry
FROM
	{{ ref("int_pinochet__drop_nulls") }} dm
GROUP BY
    {{ dbt_utils.star(
		ref("int_pinochet__drop_nulls"),
		except = ['location_n', 'location', 'latitude', 'longitude', 'exact_coordinates', 'geometry']
	)}}
