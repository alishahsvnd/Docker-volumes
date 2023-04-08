# Assignment 2
In this project, we have used Docker volumes to persist data between containers and a user-defined Docker network to enable communication between containers.

The Docker volumes were created using the docker volume create command before running the containers. The volumes were then mounted inside the containers using the --mount flag or the -v flag. We used named volumes, which are created and managed by Docker, and can be shared between containers. This allows us to persist data even if the containers are deleted or recreated.

For communication between containers, we used a user-defined Docker network. The network was created using the docker network create command, and each container was added to the network using the --network flag. By running the containers on the same network, we were able to communicate between them using their container names as hostnames.

Overall, these methods provide a reliable and scalable way to manage data and communication between Docker containers.



