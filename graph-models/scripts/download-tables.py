from pathlib import Path
from typing import Dict

import pandas as pd
from decouple import config
from sqlalchemy import URL, create_engine

POSTGRES_HOST: str = config("POSTGRES_HOST", default="localhost")
POSTGRES_USER: str = config("POSTGRES_USER", default="postgres_dev")
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="dontusemeinprod")
POSTGRES_DB: str = config("POSTGRES_DB", default="pinochet_dev")
POSTGRES_PORT: int = 5433

PROJECT_ROOT_DIR: Path = Path(__file__).parent.parent

POSTGRES_URL = URL.create(
    drivername="postgresql",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
)


def download_tables() -> Dict[str, pd.DataFrame]:
    engine = create_engine(POSTGRES_URL)

    tables = [
        "api.stg_pinochet__base",
        "api.stg_pinochet__paths",
    ]

    for t in tables:
        df = pd.read_sql(f"SELECT * FROM {t}", engine)
        df.to_csv(PROJECT_ROOT_DIR / "resources" / f"{t}.csv", index=False)
        df.to_feather(PROJECT_ROOT_DIR / "resources" / f"{t}.feather")


if __name__ == "__main__":
    download_tables()
