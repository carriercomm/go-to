% Status Report for Cloud Infrastructure and Cloud Security courses
% Leonid Vasilyev, <Leonid.Vasilyev@student.ncirl.ie>
% November 17, 2013

# Problem statement
At the current moment there is no interoperability between different Cloud Providers.
This fact complicates maintanance of Hybrid Cloud configurations
in a way that one must maintain separate OS configuration
per Cloud Provider and separate configuration for development environment.
Also this issue causes a negative impact on availabilty of a Hybrid Cloud solution.

# Project Summary
Provide an automated migration of an OS image between different Cloud Providers and developnet environment.
Without any changes in migrating image.

# Success Criteria
* Fully automated migration pipeline.

# In Scope
* Ubuntu 12.04
* LXC Containers
* Docker based containers

# Out of Scope
* Live migration
* Support other OS types

# Project Milestones
## Completed:
* Verify the idea
* Manually execute every step of the pipeline

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

