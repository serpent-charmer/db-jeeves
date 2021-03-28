#!/usr/bin/env bash
usr=$1
db=$usr"db"
schemacrawler --server=mysql --database="$db" -schemas=."$db"..dbo \
--host=10.11.3.3 --user=$usr --password=abc --info-level=maximum \
-c=schema --output-format=pdf -o=$db.pdf "$*"
