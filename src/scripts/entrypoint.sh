#!/usr/bin/env bash

set -o errexit
set -o pipefail
cmd="$@"

function postgres_ready(){
python << END
import sys
import psycopg2

try:
    dbname = 'postgres'
    user = 'postgres'
    password = 'postgres'
    host = 'postgres'
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=5432)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

function redis_ready(){
python << END
import sys
try:
    import redis
    con = redis.Redis(host="redis", socket_connect_timeout=1)
    con.ping()
except redis.exceptions.RedisError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

until redis_ready; do
  >&2 echo "Redis is unavailable - sleeping"
  sleep 1
done

>&2 echo "Redis are up - continuing..."

exec $cmd
