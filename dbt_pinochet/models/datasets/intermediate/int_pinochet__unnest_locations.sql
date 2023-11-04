{{ config(
    materialized = 'view',
) }}

SELECT
	{{ dbt_utils.star(
		from=ref("int_pinochet__construct_geometries"),
		except=["place_1", "place_2", "place_3", "place_4", "place_5", "place_6", "location_1", "location_2", "location_3", "location_4", "location_5", "location_6", "latitude_1", "latitude_2", "latitude_3", "latitude_4", "latitude_5", "latitude_6", "longitude_1", "longitude_2", "longitude_3", "longitude_4", "longitude_5", "longitude_6", "exact_coordinates_1", "exact_coordinates_2", "exact_coordinates_3", "exact_coordinates_4", "exact_coordinates_5", "exact_coordinates_6", "geometry_1", "geometry_2", "geometry_3", "geometry_4", "geometry_5", "geometry_6"]) }}
    AS place,
    "location",
    latitude,
    longitude,
    exact_coordinates,
    {{ adapter.quote("geometry") }},
    location_n
FROM
    {{ ref("int_pinochet__construct_geometries") }},
    unnest(
        ARRAY[place_1, place_2, place_3, place_4, place_5, place_6],
        ARRAY[location_1, location_2, location_3, location_4, location_5, location_6],
        ARRAY[latitude_1, latitude_2, latitude_3, latitude_4, latitude_5, latitude_6],
        ARRAY[longitude_1, longitude_2, longitude_3, longitude_4, longitude_5, longitude_6],
        ARRAY[exact_coordinates_1, exact_coordinates_2, exact_coordinates_3, exact_coordinates_4, exact_coordinates_5, exact_coordinates_6],
        ARRAY[geometry_1, geometry_2, geometry_3, geometry_4, geometry_5, geometry_6]
    ) WITH ORDINALITY AS x (place, "location", latitude, longitude, exact_coordinates, "geometry", location_n)
