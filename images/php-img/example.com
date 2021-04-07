server {
        listen 8000;
	listen [::]:8000;
        root /var/www/html;
        index index.php index.html index.htm index.nginx-debian.html;
	server_name _;

        location / {
                try_files $uri $uri/ =404;
        }

	location ~ \.(php|html|htm)$ {
		include snippets/fastcgi-php.conf;
                fastcgi_pass unix:/var/run/php/php8.0-fpm.sock;
		include fastcgi_params;
	}


        location ~ /\.ht {
                deny all;
        }
}
