FROM postgres:17.5-alpine3.21

# Apply latest APK security patches available at build time.
RUN apk update && apk upgrade --no-cache

COPY init.sql /docker-entrypoint-initdb.d/init.sql
