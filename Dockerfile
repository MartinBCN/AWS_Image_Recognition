FROM amazonlinux:latest

WORKDIR '/app'

COPY package.json .
RUN npm install

COPY . /app