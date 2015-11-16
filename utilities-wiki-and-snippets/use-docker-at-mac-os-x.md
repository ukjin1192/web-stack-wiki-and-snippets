#### Install docker

- Download docker at <a href="https://www.docker.com/docker-toolbox" target="_blank">this site</a>
- Docker will install with VirtualBox


#### Docker command

~~~
# Search image
$ docker search {IMAGE NAME}

# Download image
$ docker pull {IMAGE NAME}

# List-up whole image
$ docker images

# Remove image
$ docker rmi {IMAGE NAME}

# Create container
$ docker run -i -t --name {CONTAINER NAME} {IMAGE NAME} /bin/bash

# List-up whole container
$ docker ps -a

# Remove container
$ docker rm {CONTAINER NAME}

# Re-run stopped container
$ docker start {CONTAINER NAME}

# Restart container
$ docker restart {CONTAINER NAME}

# Attach container
$ docker attach {CONTAINER NAME}

# Stop container
$ docker stop {CONTAINER NAME}

# Create imagefile
$ vi Dockerfile [Fill out contents]
$ docker build --tag {IMAGE NAME}:{VERSION}
~~~~
