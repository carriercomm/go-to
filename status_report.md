% Status Report for Cloud Infrastructure and Cloud Security courses
% Leonid Vasilyev, <Leonid.Vasilyev@student.ncirl.ie>
% November 17, 2013

# Problem statement
At the current moment there is no OS configuration interoperability between different Cloud Providers.
This fact complicates maintanance of Hybrid Cloud configurations
in a way that one must maintain separate OS configuration
per Cloud Provider and separate configuration for development environment.
Also this issue causes a negative impact on availabilty of a Hybrid Cloud solution.

# Project Summary
Provide an automated migration of an OS image between different Cloud Providers and developnet environment.
Without any changes in migrating image.

# Success Criteria
Functional and fully automated OS image migration pipeline with the following stages: Export, Transfer and Import.

# Evaluating Approach
There are two common apporaches to maintain configuration consistency:

1. Using configuration system (CFEngine, Puppet or Cheff)
2. Nested virtualization

## Configuartion System
Pros:
* OS agnostic (as long as configuration is provided)
* Ability to deploy fine-grain changes in real-time mode
* Parallism & low network overhead. Every host is independent

Cons:
* Complexity: separate configuration for different cloud providers
* Lack of atomicity. No control over the configuration change execution
* No clean roll-back procedure

## Netsted Virtualization
Pros:
* Amoticity of changes
* Clear roll-back procedure
* Simplicity: No need to maintain separate configuration per Cloud Provider.
* Abality to execute deep secutity analysis
* Contorol over consumed resources

Cons:
 * General system overhead
 * Requires guest OS kernel support

# In Scope
* Support Ubuntu 12.04
* Support LXC Containers
* Use Docker for containers configuration

# Out of Scope
* Live migration between Cloud Providers
* Support for other Linux Distributions

# Project Milestones
## Completed:
* Verify the ability to bootstrap a linux container in VirualBox, Amazon EC2 and Windows Azure
* Manually create an LXC snapshot and move it between cloud providers
* Verify the ability to set up container via Docker in VirualBox, Amazon EC2 and Windows Azure
* Manually export container via Docker and import it under different Cloud Provider


## In Progess:
* Provide script for configurataion of Guest os in VirtualBox, Amazon Ec2 and Windows Azure
* Build API for every stage of the pipeline

## TODO:
* Prove CLI tool on top of the API


# References
Below are the links to major components used in this project.
* Project Home: https://github.com/lvsl/go-to
* Project Specification: https://github.com/lvsl/go-to/blob/master/SPEC.md
* LXC: http://linuxcontainers.org/
* Docker: https://www.docker.io/
* Cgroups: https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt

