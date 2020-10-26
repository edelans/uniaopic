#!/bin/bash
app="docker.uniao"
docker build -t ${app} .
docker run -d 
  -p 56733:80 \
  --name=${app} \
  ${app}
