#!/usr/bin/bash
version="16.14.2"
archive_name="schemacrawler-$version-distribution"
url=https://github.com/schemacrawler/SchemaCrawler/releases/download/"v"$version/$archive_name".zip"
sc_file="_schemacrawler/schemacrawler.sh"

if ! [ -x "$(command -v ./schemacrawler)" ]; then
    wget --backups=0 -nd $url -O ~/$archive_name".zip"
    unzip ~/$archive_name -d ~/
    cp ./setup/schemacrawler.sh ~/$archive_name/$sc_file
    sudo ln -s -f ~/$archive_name/$sc_file /usr/local/bin/schemacrawler
else
    echo "schemacrawler already installed"
fi
