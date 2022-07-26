./scripts/build_all.sh
./scripts/create_db_net.sh
./scripts/mysql.sh
./scripts/postgresql.sh
cp ./services/db_jeeves.service /etc/systemd/system
cp ./schemacrawler /usr/local/bin
groupadd docker
groupadd webdev
usermod -aG docker db_jeeves_user
usermod -aG webdev db_jeeves_user
chgrp -R webdev .
chmod -R 770 .
chmod -R 777 images/
chgrp webdev /usr/local/bin/schemacrawler

systemctl enable db_jeeves.service
systemctl daemon-reload
systemctl start db_jeeves.service

python3 ./scripts/refresh_db_containers.py

echo "DONE"
