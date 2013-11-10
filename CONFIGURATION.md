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
    
