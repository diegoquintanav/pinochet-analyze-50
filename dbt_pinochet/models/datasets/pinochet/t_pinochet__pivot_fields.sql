{{ config(
    materialized = 'table',
	enabled=false,
) }}

SELECT
	{{ dbt_utils.star(from=ref("t_pinochet__split_fields"), except=["field_number", "field_name"]) }},
    {{ dbt_utils.pivot(
        column = 'field_name',
		agg = 'array_agg',
		then_value='value',
        values = dbt_utils.get_column_values(
			table = ref('t_pinochet__split_fields'),
			column = 'field_name',
			where = "field_name != 'geo_location'"
			)
	) }}
FROM
	{{ ref('t_pinochet__split_fields') }}
group by {{ dbt_utils.star(from=ref("t_pinochet__split_fields"), except=["field_number", "field_name"]) }}