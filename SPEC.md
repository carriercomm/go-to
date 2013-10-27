Specification
=============

Goal of the project:
-------------------

Provide a tool for seamless migration of linux containers between different Cloud Providers.

Initial Features:
----------------

* Support container import to/export from AWS EC2
* Support container import to/export from Azure VMs
* Document Security Concers of container migration

Workflow:
--------

    Vagrant VM:                            AWS EC2 VM:
    +----------------+                     +---------------+
    |  +----------+  |    (1)              |  +---------+  |
    |  |    C0    |<------------+------------>|    C1   |<-------.   
    |  +----------+  |          |          |  +---------+  |     |
    +----------------+          |          +---------------+     | 
                                |                                |
                                |                                | (2)
                                |          Azure VM:             |
                                |          +---------------+     |
                                |          |  +---------+  |     |
                                '------------>|    C2   |<-------'
                                           |  +---------+  |
                                           +---------------+
                                           
1. Move container to cloud(s) and back to development env. 
2. Move container between cloud(s)

GoTo Architecture:
----------------

    +---------------+ +-------------+ +------------------------+
    | GoTo CLI Tool | | GoTo Web UI | | GoTo Remote Cntrl srv  |
    +---------------+ +-------------+ +------------------------+
    +----------------------------------------------------------+
    | GoTo API                                                 |
    +----------------------------------------------------------+
    +--------+ +-------------+ +-------------+ +---------------+
    | Docker | | LXC Toolkit | | AWS Toolkit | | Azure Toolkit |
    +--------+ +-------------+ +-------------+ +---------------+
    +----------------------------------------------------------+
    | Guest OS                                                 |
    +----------------------------------------------------------+
    
