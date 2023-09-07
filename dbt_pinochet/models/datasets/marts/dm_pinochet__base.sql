{{ config(materialized = "table")}}

SELECT
	*
FROM
	{{ ref("int_pinochet__drop_nulls") }}
