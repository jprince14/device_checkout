#!/bin/bash

mkdir -p certs
openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 \
  -nodes -keyout certs/server.key -out certs/server.crt -subj "/CN=example.localhost" \
  -addext "subjectAltName=DNS:example.localhost,DNS:*.localhost,IP:127.0.0.1"