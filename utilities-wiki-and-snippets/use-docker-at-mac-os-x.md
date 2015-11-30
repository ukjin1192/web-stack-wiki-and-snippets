#### Install docker

- Download docker at <a href="https://www.docker.com/docker-toolbox" target="_blank">this site</a>
- Docker will be installed with VirtualBox


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
$ docker run -i -t -p {EXPOSING PORT} --name {CONTAINER NAME} {IMAGE NAME} {COMMAND(e.g. /bin/bash)}

# List-up whole container
$ docker ps -a

# Rename container
$ docker rename {ORIGINAL CONTAINER NAME} {NEW CONTAINER NAME}

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

# Create image
$ vi Dockerfile [Fill out contents]
$ docker build --tag {IMAGE NAME}:{TAG}

# Create image from existing container
$ docker commit {CONTAINER NAME} {NEW IMAGE NAME}:{TAG}

# Check exposing port of container
$ docker port {CONTAINER NAME}

# Detach container
(In container) Ctrl-P + Ctrl-Q

# Start new shell on running container
$ docker exec -it {CONTAINER NAME} /bin/bash
~~~~
