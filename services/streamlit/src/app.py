import geopandas as gpd
import pandas as pd
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
    SELECT
        latitude,
        longitude,
        occupation_detail,
        geometry,
    FROM
        dbt_dev.dm_pinochet__base tpul
    LIMIT 10;
    """
    df = pd.read_sql(sql=query, con=engine)
    df["geometry"] = df["geometry"].apply(wkb.loads)
    df = gpd.GeoDataFrame(df, geometry="geometry")
    return df


df = get_data()

st.dataframe(df)

st.map(df)
