{{ config(
    materialized = 'table',
) }}
-- https://github.com/dbt-labs/dbt-utils#unpivot-source
{{ dbt_utils.unpivot(
    relation = ref("t_pinochet__construct_geometries"),
    cast_to = 'text',
    exclude = ['individual_id', 'group_id', 'start_date_daily', 'end_date_daily', 'start_date_monthly', 'end_date_monthly', 'last_name', 'first_name', 'minor', 'age', 'male', 'occupation', 'occupation_detail', 'victim_affiliation', 'victim_affiliation_detail', 'violence', 'method', 'interrogation', 'torture', 'mistreatment', 'targeted', 'press', 'war_tribunal', 'number_previous_arrests', 'perpetrator_affiliation', 'perpetrator_affiliation_detail', 'nationality', 'page', 'additional_comments'],
    field_name = 'field',
    value_name = 'value'
) }}

