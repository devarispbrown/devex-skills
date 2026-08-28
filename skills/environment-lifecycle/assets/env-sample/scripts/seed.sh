#!/usr/bin/env bash
set -euo pipefail

STAGE="${1:-local}"

echo "seeding deterministic demo data for ${STAGE}"
psql "${DATABASE_URL:?DATABASE_URL required}" -f "./db/seeds/${STAGE}.sql"
