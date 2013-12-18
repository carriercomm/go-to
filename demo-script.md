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
    
    

