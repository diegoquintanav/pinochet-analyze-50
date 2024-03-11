FROM ontop/ontop:latest

ENV ONTOP_ONTOLOGY_FILE=/opt/ontop/input/mapping.protege.ttl
ENV ONTOP_MAPPING_FILE=/opt/ontop/input/mapping.protege.obda
ENV ONTOP_PROPERTIES_FILE=/opt/ontop/input/mapping.protege.properties
ENV ONTOP_PORTAL_FILE=/opt/ontop/input/mapping.protege.portal.toml
ENV ONTOP_CORS_ALLOWED_ORIGINS="*"
ENV ONTOP_DEV_MODE="false"
# files needed by ontop to map the ontology to the db
COPY ./input/* /opt/ontop/input/
# postgres jdbc driver to connect to postgis
COPY ./jdbc/* /opt/ontop/jdbc/

EXPOSE 8080