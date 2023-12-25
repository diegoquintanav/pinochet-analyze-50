{{ config(materialize="table") }}

SELECT DISTINCT
    {{
        dbt_utils.generate_surrogate_key(
            [
                "event_id",
                "individual_id",
                "group_id",
                "start_date_daily",
                "end_date_daily",
                "violence",
                "method",
                "interrogation",
                "torture",
                "mistreatment",
                "targeted",
                "press",
                "war_tribunal",
                "number_previous_arrests",
                "perpetrator_affiliation",
                "perpetrator_affiliation_detail",
                "page",
            ]
        )
    }} AS pk,
    {{ adapter.quote("event_id") }},
    {{ adapter.quote("individual_id") }} AS "victim_id",
    {{ adapter.quote("group_id") }},
    {{ adapter.quote("start_date_daily") }},
    {{ adapter.quote("end_date_daily") }},
    {{ adapter.quote("violence") }},
    {{ adapter.quote("method") }},
    {{ adapter.quote("interrogation") }},
    {{ adapter.quote("torture") }},
    {{ adapter.quote("mistreatment") }},
    {{ adapter.quote("targeted") }},
    {{ adapter.quote("press") }},
    {{ adapter.quote("war_tribunal") }},
    {{ adapter.quote("number_previous_arrests") }},
    {{ adapter.quote("perpetrator_affiliation") }},
    {{ adapter.quote("perpetrator_affiliation_detail") }},
    {{ adapter.quote("page") }}
FROM {{ ref("stg_pinochet__base") }}
ORDER BY event_id
