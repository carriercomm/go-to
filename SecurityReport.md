% Go-To: Cloud Provider agnostic system migration pipeline. Security Analisys.
% Leonid Vasilyev, <Leonid.Vasilyev@student.ncirl.ie>
% December 13, 2013

#Project Summary
## Problem Statement
Different Public Cloud Providers have different and not interoperable configuration and format of Guest OS images.
This causes a “Vendor Lock-in” effect.

In case of linux system configuration of Guest OS is different for Amazon Ec2 and Windows Azure.
After performing a snapshot of a live system it's not possible to resume this image in different cloud
provider or in your local environment.
The image will not boot unless you use the same hypervisor with identical configuration.

It is a potential risk for every business operating in the Public Cloud at IaaS level.
For Hybrid Cloud deployments the above aspect causes an operational complexity.
An owner of a hybrid setup must maintain separate OS configuration for its Private and Public parts of infrastructure.
In critical scenarios such as a company or organization required to switch from one Public Cloud provider to another
time and engineering effort should be spent to create a new configuration and deployments for a new cloud infrastructure.

## Project Goal
Provide an automated migration pipeline for OS images between different Cloud Providers.
Develop a threat model, analyse related security risks and mitigation techniques.

## In Scope

* Amazon AWS and Windows Azure Public Cloud providers are used
* Ubuntu Linux 12.04 LTS is used in this project as a Guest OS
* Vagrant on top of VirtualBox is used as a local Private Cloud
* Docker is used to manage Linux Containers in the Guest OS
* VPN tunnel between Cloud Providers is used to transfer OS images.

## Architectire Overview

!["Architecture Overview"](HybridCloudOverview.jpg)

# Security analysis
## Approach & Planning

Microsoft Threat Modeling Process was used for threat modeling.
It has the following stages:

1. Identify Security Objectives
2. Perform an application design overview
3. Perform a decomposition
4. Identify Threats
5. Identify Vulnerabilities

STRIDE was used to perform a decomposition of a system.
DREAD was used to perform a ranking of found security threats.

### Identify Security Objectives

The main security objective is to prevent data leakage outside Guest OS or secure storage.

According to NIST:
"Migrating data directly from one cloud system to another
will require standards for federated identity, delegation of trust,
and secure third-party data transfers".

### Design Overview

See diagram in previous section

### Decomposition

The data in container can be split in two categories: system's data and user's data.

### Identifying Threats

Following STRIDE classication scheme, the following groups of threat should be considered:

#### Spoofing Identity

This is high risk. Currently there is no notion of identity in Docker.
This feature is on the team's backlog: <https://github.com/dotcloud/docker/issues/2700>

#### Tampering with Data

This is high risk. One can interface container archive and inject malware into it.
This can be mitigated by signing, encrypting and providing checksum of a container.

#### Repudiation

This threat is minimal.
Docker which used to lauch a container maintains full log of commands executed in container.

#### Information Disclosure

This risk is very high. Even if container encrypted and signed nothing prevents an application deployed 
in a partucular container to emit sensitive informainto into container.
To mitigate this all containers should be configured in a such a way that all state in stored outside the container.

#### Denial of Service

The risk is medium. Containers provide rich controls to configure limits for various resources, although
this configuration might be very complex.

#### Elevation of Privilege

The risk in high. Containers operate under privilidged user (root).
To mitigate this configuration of LXC should be changed from "Open by default" to "Closed by default"
see: <https://github.com/lxc/lxc/blob/master/config/templates/ubuntu.common.conf.in#L18> for such example.

### Identifying Vulnerabilities

Searching on NIST NVD resulted in just a few CVEs:
* <http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2011-4080&cid=1>
* <http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2012-3449&cid=3>

## Selection of Tools, Methodologies and Frameworks for Security Testing

I picked Microsoft Threat Modeling Process because it's very practical and well documented.
It suggests using STRIDE and DREAD which are also very practical compared to OCTAVE or CVSS.

For data encyption OpenSSL was chosen. It's a very well documented and tested crypto library.

For testing the folling tools were used:

* tcpdump for network sniffing
* ApacheBench for benchmarking HTTP services
* Custom Python scripts for DoS attacks

System was hardened using AppArmor which is a Mandatory Access Control (MAC) system
available in Linux since 2.6.36 kernel.

AppArmor provides a security model in which user is to bind access control attributes to programs rather than to users.
AppArmor confinement is provided via profiles loaded into the kernel, typically on boot.
AppArmor profiles can be in one of two modes: enforcement and complain.
Profiles loaded in enforcement mode will result in enforcement of the policy defined in the profile as well as reporting policy violation attempts (either via syslog or auditd).

AppArmor is easier to configure than SELinux or SMACK (both are also MAC systems).

## Technical Testing Approach

Testing was done on two instances: one in Amazon EC2 another in Windows Azure.
The Firefox was running in a container over VNC remote desktop.
Using `tcpdump` I was able to capture all packets coming from a particular container.

After configuring some resource limits (CPU & Memory) I started Apache web server which was serving a single
100MB file with enabled gzip compression with disabled caching.
Around 100RPS (requests per second) the container stopped responding to queries exhasted all allocated resources.
No futher grow of resources was detected.

After that I tried to exhaust disk space and network bandwith.
I was able to produce "Elephant flow", serving large file so effectevly all traffic was block by this flow.

Disk was exhausted as well pretty easily, there was no default policies to limit the size of container.

## Findings & Risk Rating

### Findings

First of all. In System Virtualization solution I picked (LXC & Docker)
the majority of security features are turned off by default.
One have to explicitly enable security fatuatures.

Network isolation is pretty clear and well designed.
When container is created you have an option to explicitly map which ports (wither TCP or UDP) should be visible
outside of container.

Disk quotes should be configured separately using advanced features of some file systems.

### DREAD Risk Rating

## Challenges & Limitations

The main challenge during threat modeling was the fact that
it's impossible at IaaS level indetify few major Security Objectvies
such as Indentity Abuse, Privacy, Financial Regulations and Reputation risks.
These objectives should be managed at SaaS level.
For example as IaaS level generated data is just a blob of bits.
So all data should be assumed sensetive by default and treated accordingly.

The other challenge was managing the private keys for both cloud providers.
Amazon Ec2 and Windows Azure uses different mechanisms for user authentication and
authorization.
In both services I had to expose (upload to cloud managnemt console) my private cerificates.
Also, there is no clear way to automate this procedure.
So deploying such solution in organization with many developers whould be a challenge.

## Outcome

I was not satisfied with the levels of security provided by System Virtualization
related to resource isolation & multitenancy.

Encryption and container signing of containers work well.

## Conclusion

System Virtualization opens up new possibilities for auditing applications at IaaS level,
inspecting activity and provide a fine grain mechanish to control resource consumption.
System Virtualization also creates an opprotunities for Cloud Brokers and Cloud Auditors
(for definitions see "NIST Reference Architecture").
On the other hand it's not widely used in production deployments yet
(there some early adopters - usually PaaS providers).
Security is a major part of System Virtualization infrastructure,
but to configure it properly one must have a deep understandings of a particular system's internals.
Nevetheless System Vitualization might be de-facto standard for deploing systems in the Public Cloud
as it allows to avoid Vendor Lock-In effect at Operating System level.


## References

### Papers

Jansen, Wayne, and Timothy Grance. "Guidelines on security and privacy in public cloud computing." NIST special publication (2011): 800-144.

Liu, Fang, et al. "NIST cloud computing reference architecture." NIST special publication 500 (2011): 292.

Brunette, G., and R. Mogull. "Security Guidance for critical areas of focus in Cloud Computing V3.0. CSA (Cloud Security Alliance), USA (2011)."


### Web resources

<http://msdn.microsoft.com/en-us/magazine/cc163519.aspx>

<https://www.owasp.org/index.php/Threat_Risk_Modeling#Identify_Threats>

<https://wiki.ubuntu.com/AppArmor>

