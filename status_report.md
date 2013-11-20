% Status Report for Cloud Infrastructure and Cloud Security courses
% Leonid Vasilyev, <Leonid.Vasilyev@student.ncirl.ie>
% November 17, 2013

# Problem statement
At the current moment there is no OS configuration and image format interoperability between different Cloud Providers.
This fact complicates maintenance of Hybrid Cloud deployments:
* User must maintain separate OS configuration per Cloud Provider and for development environment
* User is unable to migrate system to a different Cloud Provider for testing or evaluation

The above issues cause a negative impact on availability of a Hybrid Cloud solution.

# Project Summary
Provide an automated migration of an OS image between different Cloud Providers and development environment
without any changes in migrating OS image format or configuration.
Develop a threat model, analyse related security risks and mitigation techniques

# Success Criteria
Functional and fully automated OS image migration pipeline with the following stages: Export, Transfer and Import.
Sensitive data is secured and not exposed during the migration.
All stages of pipeline are externally auditable.

# Approach
Additional layer of virtualization called `System Virtualization` will be used in this project to provide core functionality.

## Approach Evaluation
###Pros:
* Atomicity of changes
* Clear roll-back procedure
* Simplicity: No need to maintain separate configuration per Cloud Provider
* Ability to execute deep security analysis via monitoring container's activity
* Control over consumed resources

###Cons:
* General system overhead
* Requires support from kernel of OS
* Potential exposure of sensitive data during migration

## Security Aspects
Security mechanisms should be integrated into the migration pipeline
to guarantee Confidentiality, Integrity, and Availability (CIA) of data.
###Threat Model:
* Service Model - IaaS
* Deployment Model - Hybrid
###Risks Assessment:
* Major risk - exposing sensitive data during migration of a container
* Major risk - Deploying container with malware from untrusted source
###Risks Mitigation:
* Build "air gap" between container and sensitive data
* Encrypt sensistive data. Inject keys into trusted container to access encrypted data
* Require authentication and authorization for activating any stage of the pipeline
* Log every changes in the pipeline for later audit

# In Scope
* Support Ubuntu Linux 12.04 LTS
* Support LXC Containers
* Support Amazon Ec2 and Windows Azure Cloud Providers
* Use Docker for containers configuration
* Provide tools to audit migration of a container
* Provide tools to prevent exposure of sensitive data
* Focus on IaaS model

# Out of Scope
* Live migration between Cloud Providers
* Support for other Linux Distributions
* Support for other OS (FreeBSD, Solaris, Windows)
* Secure migration of sensitive data
* PaaS Model

# Project Milestones
## Completed:
* Verify the ability to bootstrap a linux container in VirualBox, Amazon EC2 and Windows Azure
* Manually create an LXC snapshot and move it between Cloud Providers
* Verify the ability to set up container via Docker in VirualBox, Amazon EC2 and Windows Azure
* Manually export container via Docker and import it in different Cloud Provider

## In Progress:
* Provide script for configuration of Guest OS in VirtualBox, Amazon Ec2 and Windows Azure
* Build API for every stage of the pipeline

## Planned:
* Provide a CLI tool on top of the API
* Add functionaly to track changes and API for auditing
* Build mechanism to provide "air gap" for sensetive data

# About The Author
Software Development Engineer, with 5.5 years of experience in large multi-datacenter scale environments. 

# References
* [Project Home](https://github.com/lvsl/go-to)
* [Project Specification](https://github.com/lvsl/go-to/blob/master/SPEC.md)
* [System Level Virtualization](http://en.wikipedia.org/wiki/Operating_system-level_virtualization)
* [LXC](http://linuxcontainers.org/)
* [Docker](https://www.docker.io/)
* [Cgroups](https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt)
* [The failure of operating systems and how we can fix it](http://lwn.net/Articles/524952/)
* [CSA Guide v3.0](https://cloudsecurityalliance.org/guidance/csaguide.v3.0.pdf)
