# pinochet-analyze

![dbt-badge](https://github.com/diegoquintanav/pinochet-analyze-50/actions/workflows/dbt-docs-generate.yml/badge.svg)

A repository for exploring the pinochet dataset [freire2019pinochet] and hopefully more data. Read more about this dataset in <https://github.com/danilofreire/pinochet>.

## Main highlights

- [dbt documentation](https://diegoquintanav.github.io/pinochet-analyze-50/dbt_docs)
- [Elementary Report](https://diegoquintanav.github.io/pinochet-analyze-50/elementary) using [Elementary](https://www.elementary-data.com/)
- [FastAPI Docs](https://pinochet-api.fly.dev/docs) hosted on [fly.io](https://fly.io)
- [Graphql endpoint](https://pinochet-api.fly.dev/graphql) using [strawberry-graphql](https://strawberry.rocks/)


## Development

This project follows a monorepo structure. The main services are:

- [`pinochet-rettig-fastapi`](#pinochet-rettig-fastapi): A fastapi service to serve the data as a REST API.
- [`pinochet-rettig-linked-data`](pinochet-#rettig-linked-data): A virtual knowledge graph to query the data with SPARQL.
- [`pinochet-rettig-dbt`](#pinochet-rettig-dbt): A dbt project to transform the raw data into actionable data.
- [`postgis`](#postgis): A postgis instance to store the data.
- ['metabase'](#metabase): A metabase instance to explore the data visually.
- [`pinochet-rettig-streamlit`](#pinochet-rettig-streamlit): A streamlit app to explore the data visually.

Each service has its own `Dockerfile` and `docker-compose.yml` file to run locally. You can explore commands in the `Makefile` in the root directory. For those projects that use python, you can use `poetry` to manage the dependencies.

### Using poetry and pipx

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

See the credentials being used in the [settings.py file](https://github.com/diegoquintanav/pinochet-analyze-50/blob/main/pinochet-rettig-fastapi/src/pinochet/settings.py) and those set in the postgis instance set in [docker-compose.postgis.yml](https://github.com/diegoquintanav/pinochet-analyze-50/blob/main/docker-compose.postgis.yml)

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

These services are deployed locally using docker compose. You can start them with `docker compose -f <docker-compose-file>.yml up -d`. 

You need to provide a valid `.env` file, see `example.env` for an example.

### Postgis {#postgis}

A database with postgis extension enabled. The database is empty by default, and it is populated by dbt with

```bash
docker compose -f docker-compose.postgis.yml up -d
dbt build --target dev
```

### pinochet-rettig-dbt {#pinochet-rettig-dbt}

We use dbt to transform the raw csv into actionable data. The models are in `./models`. You can run the models with

```bash
dbt deps
dbt build --target dev
```

### Virtual knowledge graph {#pinochet-rettig-linked-data}

We use ontop to serve a virtual knowledge graph to query the database with SPARQL.

```bash
cp .env.example .env
cp ./pinochet-rettig-linked-data/ontop/input/mapping.protege.properties.example ./pinochet-rettig-linked-data/ontop/input/mapping.protege.properties
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

### FastAPI {#pinochet-rettig-fastapi}

We use fastapi to serve the data as a REST API. You can start the service with

```bash
make api.upd
```

Check the necessary configuration parameters in the docker compose file.

#### Using devcontainers (experimental)

Install the devcontainer CLI with

```bash
npm install -g devcontainer-cli
```

and run `devcontainer open` to start the a visualstudio code instance from the fastapi service at `/app/`.

> [!NOTE]
> The whole repository is mounted inside in `/workspaces/` but the application is being run from `/app/`.
> I need to figure out yet a clean workflow, but so far it is working.


#### Authentication

Authentication is done using JWT. You can get a token with the credentials for [a default user created as a migration script](./pinochet-rettig-fastapi/alembic/versions/20240302_1709427186_4101c905126c_create_daniel_lopez_as_user.py)


#### GraphQL

We use strawberry-graphql to serve the data as a GraphQL API. It is located under `localhost:8000/graphql`.

> Note: the graphql endpoint is still in progress. It accepts very few queries at the moment

#### Deployment with fly.io

I'm using fly.io to deploy the services. The configuration is in `fly.toml` files inside `./pinochet-rettig-fastapi` and `./postgis`.

You must install the flyctl cli tool to deploy the services. See <https://fly.io/docs/getting-started/installing-flyctl/> for details. After installing the cli tool, you can deploy the services with

```bash
cd pinochet-rettig-fastapi
flyctl deploy
```

and

```bash
cd postgis
flyctl deploy
```

You will need to set the `POSTGRES_PASSWORD` secret for the fastapi deployment, with `flyctl secrets set`. Note that other secrets were set by fly.io automatically, you can check them with `flyctl secrets list`:

```bash
$ cd pinochet-rettig-fastapi
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


### Metabase {#metabase}

We can use metabase to explore the data visually. You can start metabase with

```bash
docker compose -f docker-compose.postgis.yml -f docker-compose.metabase.yml up -d
```

And go to <localhost:3010> to explore the data. Metabase will ask you to create an admin user and setup the database connection.

![Example metabase chart](./img/01-example-metabase-chart.png)

### Streamlit {#pinochet-rettig-streamlit}

We use streamlit to explore the data visually. You can start the service with

```bash
docker compose -f docker-compose.postgis.yml -f docker-compose.streamlit.yml up -d
```