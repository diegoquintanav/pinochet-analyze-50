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
    b.{{ adapter.quote("event_id") }},
    b.{{ adapter.quote("individual_id") }},
    b.{{ adapter.quote("group_id") }},
    b.{{ adapter.quote("start_date_daily") }},
    b.{{ adapter.quote("end_date_daily") }},
    b.{{ adapter.quote("violence") }},
    b.{{ adapter.quote("method") }},
    b.{{ adapter.quote("interrogation") }},
    b.{{ adapter.quote("torture") }},
    b.{{ adapter.quote("mistreatment") }},
    b.{{ adapter.quote("targeted") }},
    b.{{ adapter.quote("press") }},
    b.{{ adapter.quote("war_tribunal") }},
    b.{{ adapter.quote("number_previous_arrests") }},
    b.{{ adapter.quote("perpetrator_affiliation") }},
    b.{{ adapter.quote("perpetrator_affiliation_detail") }},
    b.{{ adapter.quote("page") }}
FROM {{ ref("stg_pinochet__base") }} AS b
ORDER BY b.event_id
