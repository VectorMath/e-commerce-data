FROM postgres:15-alpine

COPY dumps/db_dump_v1_1_0.sql /docker-entrypoint-initdb.d/init.sql
