Configuring Guest OS
=====================
Based on Ubuntu 12.04.

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

Forward ports:

    $ ifconfig | grep -A 1 lxc
    $ sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to <lxc-ip>:<port>
    
