#!/bin/sh

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h postgres -U $POSTGRES_USER -c '\q'; do
  echo "Aguardando PostgreSQL em postgres:5432..."
  sleep 1
done

echo "PostgreSQL está disponível, executando migrações..."
alembic upgrade head