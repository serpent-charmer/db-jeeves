FROM debian:latest
RUN apt-get update 
RUN apt-get install -y lsb-release apt-transport-https ca-certificates wget
#RUN apt-get -y install wget gnupg
#RUN wget -q https://packages.sury.org/php/apt.gpg -O- | apt-key add - 
#RUN echo "deb https://packages.sury.org/php/ buster main" | tee /etc/apt/sources.list.d/php.list
RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
RUN echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list
RUN apt-get update
RUN apt-get -y install libpq-dev php8.0 php8.0-fpm php8.0-pgsql php8.0-mysql nginx

COPY ./app /var/www/html/
COPY ./example.com /etc/nginx/sites-available/default
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
RUN echo "security.limit_extensions = .php .html\nclear_env = no" >> /etc/php/8.0/fpm/pool.d/www.conf

ENTRYPOINT /etc/init.d/php8.0-fpm start \
&& /etc/init.d/nginx start > /dev/null \
&& tail -f /dev/null  
