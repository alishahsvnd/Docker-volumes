#!/bin/bash

# create client volume
docker volume create clientvol

# build and run client container
docker build -t client .
docker run -it --name client --mount source=clientvol,target=/clientdata --network my_network client