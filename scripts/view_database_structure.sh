#!/usr/bin/env bash
db=database-new-user-njphzh2e
../../_schemacrawler/schemacrawler.sh --server=mysql --database=$db -schemas=.$db..dbo --host=10.11.3.3 --user=root --password=my-secret-pw --info-level=maximum -c=schema --output-format=png -o=database-diagram.png "$*"
