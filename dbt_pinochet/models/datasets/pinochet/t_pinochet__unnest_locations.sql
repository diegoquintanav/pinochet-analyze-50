{{ config(
    materialized = 'table',
) }}

SELECT
	{{ dbt_utils.star(
		from=ref("t_pinochet__construct_geometries"),
		except=["place_1", "place_2", "place_3", "place_4", "place_5", "place_6", "location_1", "location_2", "location_3", "location_4", "location_5", "location_6", "latitude_1", "latitude_2", "latitude_3", "latitude_4", "latitude_5", "latitude_6", "longitude_1", "longitude_2", "longitude_3", "longitude_4", "longitude_5", "longitude_6", "exact_coordinates_1", "exact_coordinates_2", "exact_coordinates_3", "exact_coordinates_4", "exact_coordinates_5", "exact_coordinates_6", "geo_location_1", "geo_location_2", "geo_location_3", "geo_location_4", "geo_location_5", "geo_location_6"])}}
	place, location, latitude, longitude, exact_coordinates, geo_location, location_n
FROM
	{{ ref("t_pinochet__construct_geometries")}} t,
	UNNEST(
		ARRAY[t.place_1, t.place_2, t.place_3, t.place_4, t.place_5, t.place_6],
		ARRAY[t.location_1, t.location_2, t.location_3, t.location_4, t.location_5, t.location_6],
		ARRAY[t.latitude_1, t.latitude_2, t.latitude_3, t.latitude_4, t.latitude_5, t.latitude_6],
		ARRAY[t.longitude_1, t.longitude_2, t.longitude_3, t.longitude_4, t.longitude_5, t.longitude_6],
		ARRAY[t.exact_coordinates_1, t.exact_coordinates_2, t.exact_coordinates_3, t.exact_coordinates_4, t.exact_coordinates_5, t.exact_coordinates_6],
		ARRAY[t.geo_location_1, t.geo_location_2, t.geo_location_3, t.geo_location_4, t.geo_location_5, t.geo_location_6]
		) WITH ORDINALITY AS x(place, location, latitude, longitude, exact_coordinates, geo_location, location_n)



