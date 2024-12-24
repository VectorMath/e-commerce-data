FROM postgres:15-alpine

COPY dumps/init_scripts /docker-entrypoint-initdb.d/
