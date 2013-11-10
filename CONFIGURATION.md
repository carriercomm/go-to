Configuring Guest OS
=====================
Based on Ubuntu 12.04.

Installing packages:
-------------------
Upgrade your kernel to 3.8 installing backport apt-get.

Install new lxc via PPA: https://launchpad.net/~ubuntu-lxc/+archive/daily

    sudo add-apt-repository ppa:ubuntu-lxc/daily
    apt-get update
    sudo apt-get install lxc
    
lxc-ls is confusing:

    $ lxc-ls
    $ sudo lxc-ls
    c1
    $ sudo lxc-info c1
    Name:           c1
    State:          STOPPED
    
NOTE: lxc-ls stalls if you try to run `lxc-start -n <C>` and then close the console.

    $ sudo lxc-start -d -n <C>
    $ sudo lxc-console -n <C>
    # Will log you into a container, to quit use C-a q.
    
NOTE: the above command does not work if you lauched container(lxc-start) withod -d option.

Network setup:
--------------
Forward ports:

    $ ifconfig | grep -A 1 lxc
    $ sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to <lxc-ip>:<port>
    # in case you want to delete or change forwards:
    $ sudo iptables -t nat -D PREROUTING 1
    $ sudo iptables -t nat -L
    
NOTE: you need to provide an IP of interface in <C>.

Moving container:
-----------------
Snapshotting with lxc-snapshot:

lxc-snapshot creates, lists, and restores container snapshots.

Snapshots are deltas to original containers.


Stopping container:

    $ sudo lxc-stop -n c1 -s -t 60
    
Use this command to archive a container:

    $ sudo tar --numeric-owner -czvf c1.tgz /var/lib/lxc/c1
    
When moving that way container name shoud be uniq. You can't rename container.


Moving with Docker:
-------------------

Docker add a layer of automation on top of lxc tools.

Install Docker:

    http://docs.docker.io/en/latest/installation/ubuntulinux/
    

Migration is done via docker import / export:

    # export
    $ sudo docker export <CID> > <CID>.tar
    # import
    $ cat <CID>.tar | sudo docker import -
    $ sudo docker run -i -t <CID> /bin/bash
    


    
