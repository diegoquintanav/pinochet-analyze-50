{{ config(
    materialized = 'table',
) }}
select
	{{ dbt_utils.star(from=ref("t_pinochet__unpivot_geometries"), except=["field"]) }},
	split_part(field, '_', -1) as field_number,
	left(field, -2) as field_name
from {{ ref("t_pinochet__unpivot_geometries") }}