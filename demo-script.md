#Demo of linux containers' migration

This demonstration is done in Ubuntu 12.04 LTS

## Configuring Guest OS

Follow this guide to configure the system:

* <http://docs.docker.io/en/latest/installation/ubuntulinux/>
* <http://docs.docker.io/en/latest/installation/kernel/>

## Connecting to ec2:

    cd ~/Dev/go-to
    ssh -i openvpn-server-1.nrt.pem ubuntu@54.238.185.51
    
## Connecting to Azure:

    cd ~/Dev/go-to
    ssh -i azure/azure_goto.pem ubuntu@137.117.145.155
    
## Checking containers:

    sudo docker run -i -t ubuntu /bin/bash
    sudo docker pull ubuntu
    
## Viewing logs of container:

    sudo docker ps -a # list all containers
    sudo docker logs <container_id>
    
## Initialize containers directory:

    sudo mkdir /croot
    sudo mkdir /cdata
    
## Using Dockerfiles configurations:

### Create a Docekrfile:

    cd /croot/firefox-vnc
    cat Dockerfile
    # Firefox over VNC
    #
    # VERSION               0.3
    FROM ubuntu
    # make sure the package repository is up to date
    RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
    RUN apt-get update
    # Install vnc, xvfb in order to create a 'fake' display and firefox
    RUN apt-get install -y x11vnc xvfb firefox
    RUN mkdir /.vnc
    # Setup a password
    RUN x11vnc -storepasswd 1234 ~/.vnc/passwd
    # Autostart firefox (might not be the best way, but it does the trick)
    RUN bash -c 'echo "firefox" >> /.bashrc':w
    EXPOSE 5900
    CMD    ["x11vnc", "-forever", "-usepw", "-create"]
    
### Build container:

    sudo docker build -t vasilyev/firefox .
    
### Run a container:

    sudo docker run -name firefox-vnc -p 5900:5900 -d vasilyev/firefox
    
### Export a container:

    sudo docker export firefox-vnc > firefox-vnc.tar
    bzip2 firefox-vnc.tar
    
### Transfer archive to azure host:

    scp via my laptop
    
### Import a container as an image:

    cat firefox-vnc.tar.bz2 | sudo docker import - vasilyev/firefox
    
### Restore container after serialization:

    # It's a bug that CMD is not repated so must copy CMD line from Dockerfile
    sudo docker run -name firefox-vnc -p 5900:5900 -d vasilyev/firefox x11vnc -forever -usepw -create
    
    
    
    
    

