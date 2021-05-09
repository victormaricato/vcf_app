#!/usr/bin/env bash
set -euxo pipefail

file=$1
db=$(docker ps -aqf "name=postgres")

cat database/start_db.sql | docker exec -i $db psql -U postgres

gunzip -c $file > database/data/unziped.vcf

python3 database/populate_db.py

rm database/data/unziped.vcf
