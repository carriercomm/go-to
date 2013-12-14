% Go-To: Cloud Provider agnostic OS image migration pipeline
% Leonid Vasilyev, <Leonid.Vasilyev@student.ncirl.ie>
% December 13, 2013

#Project Summamry
## Problem Statement
Different Public Cloud Providers have different and not interoperable format of OS images.
This cause a “Vendor Lock-in” effect.
Which is a potential risk for every business operating in the Public Cloud at IaaS level.
For Hybrid Cloud deployments the above aspect causes an operational complexity.
An owner of a hybrid setup must maintain separate OS configuration for it's Privete and Public parts infrastructure.
In critical scenarios such as a company or organization required to switch from one Public Cloud provider to another.
Time and engeneering effort should be spent to create a new configuration and deplyments for a new cloud infrastructure.

## Projec Goal
Provide an automated migration pipeline for OS images between different Cloud Providers.
Develop a threat model, analyze related security risks and mitigation techniques.

## In Scope
As Public Cloud providers Amazon AWS and Windows Azure are used.

Ubuntu Linux 12.04 LTS is used in this project.
This OS version is most widly used and available from all Public Cloud Providers.

#Design
## Evaluating options
Historicall two main approached applied to provide reprodusable and consistent configuration of OS:
* Configuration Managment Systems
* Hardware Virtualization
* System Virtualization

Below is a comparison of Pros and Cons of both approaches.

###Configuration Managment Systems
These systemes began to appear in mid 90-x. CFEngine, Puppet and Cheff are most widely used today.
####Pros
- Zero overhead. All changes are applied to OS directly as soon as possible.

- Ability to apply fine grained changes to live system without stopping a service.

- Domain Specific Languages (DSL) are used for configuraton. Which allow a great degree of flexibility.

####Cons
- System configuration is performed via a large amount of small iterative changes.
  The system is "eventually" be is a desired state.

- Changes are not atomic. If system is restarted on the middle of applying change process. There is no guarantee that configuration of system will be resumed from last point

- Lack of built-in checkpointing. Althow it's possible with some file-system performed on-line backups.

- No clean roll-back procedure. Roll-back is add hoc usually done via executing different set of commands on the system

- Additional software is required to operate on a target system, usually it's a background process running under privilidged uses. Which causes a security risk.

###Hardware Virtualization
####Pros
- Live migration. It's possible to perform a lize migration of the system by suspending it's state
####Cons
- High overhead. Unless paravirtualized every subsystem has a degraded performance
- Nested virtualization is not possible. Only Linux KVM support nested virtualization. 

###System Virtualization
In System virtualization, every application or a group of applocations is isolated from each other but running in the same kernel. 
####Pros
- It's possible to use it on top of hardware virtualization
- Changes to the system are atomic
- Cleam rollback. Just revert to the revious version of a container
- It's possible to run multiple versions of the same container on the system
- Low overhead abstration.
  All abstration is done in a kernel by settings attributes to different internal data-structures.

####Cons
- No live migration. Before creatign a shanpshot all processes should be freezed in a container. There is some onging development in this area.

## Choosen design
### Why?

#Implementation of Private Cloud

Because the project doesn't require sepaearte Private Cloud infrastrucure to build a Hybrid Solution.
VirtualBox is used as a delelopment platform to "ineject" initial containers in the Hybrid Solution (Amazon AWS Ec2 + Windows Azure VM)

Vagrant used to orchestrate configuration of VMs.

Follow these steps to complete the setup.

__Install VirtualBox-4.3.4__

  * Download package for your OS from http://download.virtualbox.org/virtualbox/4.3.4/
  * Follow instruction for yous OS to install: https://www.virtualbox.org/manual/ch02.html

__Installing Vagrant-1.3.5__

  * Download and execute package for your OS from http://downloads.vagrantup.com/tags/v1.3.5

__Configuring Vagrant to run Docker-0.7.1__ 

    # this directory will only keep configuration for Vagrant. Image data stred separately
    export GOTO_WORKSPACE=$(pwd)/$USER-goto-workspace
    mkdir $GOTO_WORKSPACE
    cd $GOTO_WORKSPACE
    
    # Docker provided pre configuration for Vagrant
    wget --no-check-certificate "https://github.com/dotcloud/docker/raw/v0.7.1/Vagrantfile" -O Vagrantfile
    
    # Start VM and SSH to it
    vagrant up
    vagrant ssh # <-- this command will bring you to VM shell
    
    # !!! COMMANDS BELOW ARE EXECUTED IN VM !!!
    
    # Enable swap limit support. This is not enabled by default.
    sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"/' /etc/default/grub
    
    # Activate changes
    sudo update-grub
    sudo reboot
    
    # Check Docker status
    sudo docker info
    
    # Output should look like this:
    Containers: 0
    Images: 0
    Driver: aufs
    Root Dir: /var/lib/docker/aufs
    Dirs: 0
    
    # Congratulations! Your VM is configured to run containers. Exit the VM shell
    exit 

This guide is partially based on official Docker guide: http://docs.docker.io/en/latest/installation/

## Out of Scope
The above setup was tested on MacOSX 10.8.5

#Provisioning of Public Cloud
##Taken steps
##Monitoring options

#Implementation of Hybrid Cloud
##Architecture Overview
![Architecture Overview](HybridCloudOverview.png)

## Go-To Stack
![Go-To Stack](GoToStack.png)

## Migration

## Network Features

# Demonstration of dynamic characteristics
## Migration
  
# References
## Web resources
http://lwn.net/Articles/524952/

http://michaelwasham.com/2013/09/03/connecting-clouds-site-to-site-aws-azure/

http://blog.docker.io/2013/08/containers-docker-how-secure-are-they/

https://wiki.ubuntu.com/LxcSecurity

http://www.ibm.com/developerworks/linux/library/l-lxc-security/index.html

http://marceloneves.org/papers/pdp2013-containers.pdf

https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt

http://stackoverflow.com/questions/17989306/what-does-docker-add-to-just-plain-lxc

http://marceloneves.org/papers/pdp2013-containers.pdf

##Papers
Menage, Paul B. "Adding generic process containers to the linux kernel." Linux Symposium. 2007.
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.111.798&rep=rep1&type=pdf#page=45

Xavier, Miguel G., et al. "Performance Evaluation of Container-based Virtualization for High Performance Computing Environments." Parallel, Distributed and Network-Based Processing (PDP), 2013 21st Euromicro International Conference on. IEEE, 2013.

Shea, Ryan, and Jiangchuan Liu. "Performance of Virtual Machines Under Networked Denial of Service Attacks: Experiments and Analysis." (2013): 1-1.





