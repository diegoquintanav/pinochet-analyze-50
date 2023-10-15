import pandas as pd
import sqlalchemy as sa
from decouple import Config, RepositoryEnv
from pathlib import Path

ENV_PATH = Path(__file__).parents[3] / ".env"

config = Config(RepositoryEnv(ENV_PATH))

HOST = config("POSTGRES_HOST", default="localhost")
PORT = config("POSTGRES_PORT", default=5433)
USER = config("POSTGRES_USER", default="postgres")
PASS = config("POSTGRES_PASSWORD", default="postgres")
DB = config("POSTGRES_DB", default="pinochet")

conn = sa.create_engine(f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")

print("Reading from database")
sql = "SELECT * FROM api.stg_pinochet__base"
df = pd.read_sql(sql, conn)

CSV_PATH = Path(__file__).parent.parent / "data" / "stg_pinochet__base.csv"
print(f"Saving to {CSV_PATH}")
df.to_csv(CSV_PATH, index=False)
