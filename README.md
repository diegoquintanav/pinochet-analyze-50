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
dbt build
```

Get the dbt documentation with

```bash
make dbt_docs.devserver
```

Check other commands with `make help`.

## Services

These services are deployed locally using docker compose. You can start them with `docker compose up -d`. You need to provide a valid `.env` file, see `example.env` for an example.

### Networking between postgis and superset

We use an external network to allow superset to connect to postgis. This network is managed by docker, and it needs to be created _before_ starting the services.

```bash
docker network create nw_pinochet
```

or pass `-f docker-compose.nw_pinochet.yml` to `docker compose up -d`.

See <https://stackoverflow.com/a/67811533/5819113> and <https://superset.apache.org/docs/installation/installing-superset-using-docker-compose/#configuring-docker-compose> for more details.

Quote from the superset docs:

> Note: Users often want to connect to other databases from Superset. Currently, the easiest way to do this is to modify the docker-compose-non-dev.yml file and add your database as a service that the other services depend on (via x-superset-depends-on). Others have attempted to set network_mode: host on the Superset services, but these generally break the installation, because the configuration requires use of the Docker Compose DNS resolver for the service names. If you have a good solution for this, let us know!

### Postgis

A database with postgis extension enabled. The database is empty by default, and it is populated by dbt.

### Superset

We use a modified version of `docker-compose-non-dev.yml` with paths modified to work with this project. See <https://superset.apache.org/docs/installation/installing-superset-using-docker-compose> for details.

### Virtual knowledge graph

We use ontop to serve a virtual knowledge graph to query the database with SPARQL.

```bash
cp .env.example .env
cp ./services/ontop/input/mapping.protege.properties.example ./services/ontop/input/mapping.protege.properties
docker compose -f docker-compose.postgis.yml -f docker-compose.ontop.yml up -d
```

And go to <0.0.0.0:8083> to run an example query with the virtual knowledge graph.

```sparql
PREFIX : <http://example.org/pinochet-rettig#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?victim ?lastName {
  ?victim a :Victim ; foaf:lastName ?lastName .
}
```
