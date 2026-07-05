# Pinochet Virtual Knowledge Graph (Ontop)

SPARQL endpoint over the Pinochet-Rettig dataset using [Ontop](https://ontop-vkg.org/) as a virtual knowledge graph engine.

## What it does

Ontop maps the relational PostgreSQL/PostGIS database to an RDF graph using an OWL ontology and OBDA (Ontology-Based Data Access) mappings. This allows querying the data via SPARQL without materializing triples.

## Files

- `datasets/pinochet-rettig/semantics/mapping.protege.ttl` — OWL ontology (Event, Location, Victim, Person, Perpetrator classes)
- `datasets/pinochet-rettig/semantics/mapping.protege.obda` — OBDA mappings from SQL tables to RDF triples
- `input/mapping.protege.properties` — JDBC connection properties (created from `.example`)
- `jdbc/postgresql-42.7.1.jar` — PostgreSQL JDBC driver

## Prerequisites

1. **PostGIS container** must be running
2. **dbt API models must be built** — Ontop queries `api.api_pinochet__victim`, `api.api_pinochet__event`, `api.api_pinochet__location`. These are created by `dbt build`.

## Setup

```bash
# 1. Create the properties file from the example template
cp pinochet-rettig-linked-data/ontop/input/mapping.protege.properties.example \
   pinochet-rettig-linked-data/ontop/input/mapping.protege.properties

# 2. Ensure PostGIS is running and dbt models are built
make db.upd
dbt build --target dev --select models/datasets/api

# 3. Start Ontop
make ontop.upd
```

## Querying

The SPARQL endpoint is available at `http://localhost:8083/sparql`.

### Example query

```sparql
PREFIX : <http://example.org/pinochet-rettig#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?victim ?lastName {
  ?victim a :Victim ; foaf:lastName ?lastName .
}
```

## Current mappings

| Class | SQL Source | Properties mapped |
|-------|-----------|-----------------|
| Victim | `api.api_pinochet__victim` | `hasAge`, `hasFirstName`, `hasLastName` |
| Location | `api.api_pinochet__location` | (class assertion only) |
| Event | `api.api_pinochet__event` | (class assertion only) |

> **Note**: Object properties (`:hasVictim`, `:hasLocation`, `:hasPerpetrator`) are defined in the ontology but not yet mapped in the OBDA file. Phase 4 of the showcase roadmap will expand these.

## Troubleshooting

**Error: "Cannot find relation api.api_pinochet__victim"**

The dbt API models haven't been built. Run:
```bash
uv run dbt build --target dev --select models/datasets/api
```

**Error: mount conflict on `mapping.protege.properties`**

Ensure there is no directory named `mapping.protege.properties` in `datasets/pinochet-rettig/semantics/`. The mount expects a file, not a directory.

## Stack

- Ontop 5.5.0
- PostgreSQL 15 JDBC driver
- OWL 2 / RDF / SPARQL 1.1
