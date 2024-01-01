# pinochet-analyze

![dbt-badge](https://github.com/diegoquintanav/pinochet-analyze-50/actions/workflows/dbt-docs-generate.yml/badge.svg)

## Main highlights

- [dbt documentation](https://diegoquintanav.github.io/pinochet-analyze-50/dbt_docs)
- [Elementary Report](https://diegoquintanav.github.io/pinochet-analyze-50/elementary) using [Elementary](https://www.elementary-data.com/)
- [FastAPI Docs](https://pinochet-api.fly.dev/docs) hosted on [fly.io](https://fly.io)
- [Graphql endpoint (in progress)](https://pinochet-api.fly.dev/graphql) using [strawberry-graphql](https://strawberry.rocks/)

A repository for exploring the pinochet dataset [freire2019pinochet] and hopefully more data. Read more about this dataset in <https://github.com/danilofreire/pinochet>.

## Development

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
      schema: api

  target: dev
```

you can now run dbt models with

```bash
dbt build --target dev
```

Get the dbt documentation with

```bash
make dbt_docs.devserver
```

Check other commands with `make help`.

## Services

These services are deployed locally using docker compose. You can start them with `docker compose up -d`. You need to provide a valid `.env` file, see `example.env` for an example.


### Postgis

A database with postgis extension enabled. The database is empty by default, and it is populated by dbt with

```bash
docker compose -f docker-compose.postgis.yml up -d
dbt build --target dev
```

### dbt

We use dbt to transform the raw csv into actionable data. The models are in `./models`. You can run the models with

```bash
dbt deps
dbt build --target dev
```

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

### Metabase

We can use metabase to explore the data visually. You can start metabase with

```bash
docker compose -f docker-compose.postgis.yml -f docker-compose.metabase.yml up -d
```

And go to <localhost:3010> to explore the data. Metabase will ask you to create an admin user and setup the database connection.

![Example metabase chart](./img/01-example-metabase-chart.png)

### Superset

> Note: superset deployment is experimental, expect a few bumps along the way.

Instead of metabase, we can use a modified version of `docker-compose-non-dev.yml` with paths modified to work with this project. See <https://superset.apache.org/docs/installation/installing-superset-using-docker-compose> for details.

#### Networking between postgis and superset

We use an external network to allow superset to connect to postgis. This network is managed by docker, and it needs to be created _before_ starting the services.

```bash
docker network create nw_pinochet
```

or pass `-f docker-compose.nw_pinochet.yml` to `docker compose up -d`.

See <https://stackoverflow.com/a/67811533/5819113> and <https://superset.apache.org/docs/installation/installing-superset-using-docker-compose/#configuring-docker-compose> for more details.

Quote from the superset docs:

> Note: Users often want to connect to other databases from Superset. Currently, the easiest way to do this is to modify the docker-compose-non-dev.yml file and add your database as a service that the other services depend on (via x-superset-depends-on). Others have attempted to set network_mode: host on the Superset services, but these generally break the installation, because the configuration requires use of the Docker Compose DNS resolver for the service names. If you have a good solution for this, let us know!

## Deployment

I'm using fly.io to deploy the services. The configuration is in `fly.toml` files inside `./services/pinochet-api` and `./services/postgis`.

You must install the flyctl cli tool to deploy the services. See <https://fly.io/docs/getting-started/installing-flyctl/> for details. After installing the cli tool, you can deploy the services with

```bash
flyctl deploy
```

You will need to set the `POSTGRES_PASSWORD` secret for the fastapi deployment, with `flyctl secrets set`. Note that other secrets were set by fly.io automatically, you can check them with `flyctl secrets list`:

```bash
$ cd services/pinochet-api
$ flyctl secrets list
NAME             	DIGEST          	CREATED AT
DATABASE_URL     	xxxxxxxxxxxxxxxx	23h7m ago
POSTGRES_PASSWORD	xxxxxxxxxxxxxxxx	22h49m ago
SECRET_KEY       	xxxxxxxxxxxxxxxx	22h30m ago
SENTRY_DSN       	xxxxxxxxxxxxxxxx	21h37m ago
```

Set the `POSTGRES_PASSWORD` secret with

```bash
flyctl secrets set POSTGRES_PASSWORD=password_from_flyio_db
```

You will also need to activate the postgis extension, by connecting to the database with `flyctl pg connect` and running `CREATE EXTENSION postgis;`:

```bash
❯ fly pg connect --app pinochet-api-prod --database pinochet_api
Connecting to fdaa:3:d37e:a7b:1be:de4c:ba0b:2... complete
psql (15.3 (Debian 15.3-1.pgdg120+1))
Type "help" for help.

pinochet_api=# CREATE EXTENSION postgis;
```
