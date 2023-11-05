import datetime as dt

import geopandas as gpd
import pandas as pd
import pydeck as pdk
import streamlit as st
from decouple import config
from shapely import wkb
from sqlalchemy import create_engine

POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
POSTGRES_DB = config("POSTGRES_DB")
POSTGRES_HOST = config("POSTGRES_HOST", default="0.0.0.0")
POSTGRES_PORT = config("POSTGRES_PORT", default="5433")

db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(db_url)

st.header("Hello World!")


@st.cache_data
def get_data():
    query = """
    SELECT *
    FROM api.stg_pinochet__base t;
    """
    df = pd.read_sql(sql=query, con=engine)
    df["geometry"] = df["geometry"].apply(wkb.loads)
    df = gpd.GeoDataFrame(df, geometry="geometry")
    return df


df = get_data()


def _get_columns(df: pd.DataFrame, column: str):
    return df[column].unique().tolist()


def build_multiselect(df: pd.DataFrame, column: str):
    cols = _get_columns(df=df, column=column)
    return st.multiselect(column, options=cols, default=cols)


tab_a, tab_b = st.tabs(["Regular map", "Pydeckgl"])

with st.sidebar:
    min_start_date = df["start_date_daily"].dropna().min()
    max_end_date = df["end_date_daily"].dropna().max()

    st.slider(
        "start_date_daily",
        min_value=min_start_date,
        max_value=max_end_date,
        value=(min_start_date, max_end_date),
        step=dt.timedelta(days=1),
    )

    nationalities = build_multiselect(df=df, column="nationality")

df = df.query("nationality in @nationalities")

with tab_a:
    st.map(df)

    st.dataframe(
        df.drop(columns=["geometry"]),
        use_container_width=True,
    )

with tab_b:
    df_pydeck = df[
        [
            "individual_id",
            "latitude",
            "longitude",
            "occupation",
            "nationality",
        ]
    ].copy()

    st.dataframe(
        df_pydeck,
        use_container_width=True,
    )

    view_state = pdk.data_utils.compute_view(
        df_pydeck[["longitude", "latitude"]],
        0.1,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            tooltip={"text": "{occupation}"},
            initial_view_state=view_state,
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df_pydeck,
                    get_position="[longitude, latitude]",
                    get_radius=200,
                    get_color="[200, 30, 0, 160]",
                    pickable=True,
                ),
            ],
        )
    )
