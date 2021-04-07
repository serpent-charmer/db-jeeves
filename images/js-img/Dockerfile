FROM debian:stable
RUN apt-get update && apt-get install -y apt-transport-https 
RUN apt-get install nodejs curl -y
RUN curl -L https://npmjs.org/install.sh | sh

WORKDIR /app

RUN npm install express mysql2 pg ejs --save

COPY ./app  .

ENTRYPOINT node ./index.js
