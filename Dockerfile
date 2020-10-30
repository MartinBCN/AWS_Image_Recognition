FROM amazonlinux:latest

WORKDIR '.'

COPY . .

RUN ./compress.sh
