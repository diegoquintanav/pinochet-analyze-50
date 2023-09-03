# pinochet-analyze

A repository for exploring the pinochet dataset [freire2019pinochet] and hopefully more data. Read more about this dataset in <https://github.com/danilofreire/pinochet>.

## Setup

Install poetry with pipx and install the dependencies

```bash
# install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# install poetry
pipx install poetry

# install dependencies
poetry install
```

After installing the dependencies, you need to configure your dbt at `~/.dbt/profiles.yml`.

```yaml
# ~/.dbt/profiles.yml
dbt_pinochet:
  outputs:
    dev:
      type: postgres
      threads: 1
      host: 0.0.0.0
      port: 5433
      user: postgres
      pass: postgres
      dbname: pinochet
      schema: dbt_dev

  target: dev
```

you can now run dbt models with

```bash
dbt seed
dbt run
```

Get the dbt documentation with

```bash
make dbt_docs.devserver
```

Check other commands with `make help`.

## Services

These services are deployed locally using docker compose

### Postgis

A database with postgis extension enabled. The database is empty by default, and it is populated by dbt.

### Superset

We use a modified version of `docker-compose-non-dev.yml` with paths modified to work with this project. See <https://superset.apache.org/docs/installation/installing-superset-using-docker-compose> for details.

#### Networking between postgis and superset

We use an external network to allow superset to connect to postgis. This network is created by docker compose.
