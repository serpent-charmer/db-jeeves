FROM debian:stable
RUN apt-get update && apt-get install -y apt-transport-https curl \
 && curl -sL https://deb.nodesource.com/setup_15.x | bash - && apt-get update \
 && apt-get install nodejs -y

WORKDIR /app

RUN npm install express mysql2 pg ejs --save

COPY ./app  .

ENTRYPOINT node ./index.js
