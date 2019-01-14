#!/bin/bash

docker build -t watershed.py .
docker run --rm watershed.py
