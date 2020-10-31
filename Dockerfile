FROM amazonlinux:latest

WORKDIR '.'

COPY . .

RUN chmod +x compress.sh
RUN ./compress.sh
