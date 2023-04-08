#!/bin/bash

# create user-defined network
docker network create my_network

# create server volume
docker volume create servervol

# run mongodb container
docker run -d --name mongodb --network my_network -v mongodbdata:/data/db mongo

# build and run server container
docker build -t server .
docker run -d --name server --mount source=servervol,target=/serverdata --network my_network server