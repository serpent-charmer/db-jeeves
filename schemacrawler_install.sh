version="16.14.2"
archive_name="schemacrawler-$version-distribution"
url=https://github.com/schemacrawler/SchemaCrawler/releases/download/"v"$version/$archive_name".zip"
home_dir=/home/$(logname)
sc_file="_schemacrawler/schemacrawler.sh"

if ! [ -x "$(command -v ./schemacrawler)" ]; then
    wget --backups=0 -nd $url -O $home_dir/$archive_name".zip"
    unzip $home_dir/$archive_name -d $home_dir/
    wget --backups=0 https://raw.githubusercontent.com/serpent-charmer/SchemaCrawler/master/schemacrawler-distrib/src/assembly/schemacrawler.sh -O $home_dir/$archive_name/$sc_file
    ln -s $home_dir/$archive_name/$sc_file ./schemacrawler 
    chown -R $(logname) $home_dir/$archive_name
else
    echo "schemacrawler already installed"
fi
