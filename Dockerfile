FROM postgres:15-alpine

COPY dumps/db_dump_v1_2_2.sql /docker-entrypoint-initdb.d/init.sql
