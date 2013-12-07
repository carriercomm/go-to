#I. Project Summamry

#II. Design
## Evaluating options
## Pros
## Cons

#II. Implementation
## Challenges
## Out of Scope

#Appendix A: Setting up a local environmenrt

VirtualBox used as a local virtual development environment.
Vagrant used to orchestrate configuration of VMs.

Follow these steps to complete the setup. This guide only for Unix-like OS types.

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
    vagrant ssh
    


#Appendix B: Setting up public cloud infrastructure

#Appendix C: Go-To API Reference
