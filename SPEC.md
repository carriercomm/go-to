Specification
=============

Goal of the project:
-------------------

Provide a tool for seamless migration of linux containers between different Cloud Providers.


Initial Features:
----------------

* Support AWS
* Support Azure
* Document Security Concers


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
