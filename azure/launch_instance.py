#!/usr/bin/env python

'''
Script to launch Azure VM
'''

__author_ = "Leonid Vasilyev, <vsleonid@gmail.com>"

import json
import hashlib
import time
import sys
from datetime import datetime

import azure
from azure.servicemanagement import *

INSTANCE_CONFIG = {
    "image": "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu_DAILY_BUILD-precise-12_04_3-LTS-amd64-server-20131205-en-us-30GB",
    "type": "Medium",
}

# config is JSON file with the following fields:
#  {
#      "subscription_id": "...",
#      "api_certificate_path": "path/to/certificate/certificate.pem",
#      "cert_thumbprint": "thumbprint for another CloudService certificate",
#      "cloud_service": "globally unique CloudService name",
#      "storage_name": "globally unique storage name"
#  }


def main(config_path):
    with open(config_path) as f:
        config = json.load(f)

    name = config["cloud_service"]

    sms = ServiceManagementService(
        config['subscription_id'],
        config['api_certificate_path'])

    vhd = OSVirtualHardDisk(
        INSTANCE_CONFIG["image"],
        "http://{service}.blob.core.windows.net/{container}/{blob}.vhd".format(
            service=config['storage_name'],
            container=name,
            blob="os"
        ).lower().replace("_", "-").replace("--", "-")
    )

    linux_config = LinuxConfigurationSet(
        name,
        "ubuntu",
        name, # will not be used
        disable_ssh_password_authentication=True)

    publickey = PublicKey(
        config['cert_thumbprint'],
        "/home/ubuntu/.ssh/authorized_keys") # file on VM
    linux_config.ssh.public_keys.public_keys.append(publickey)

    network = ConfigurationSet()
    network.configuration_set_type = 'NetworkConfiguration'
    network.input_endpoints.input_endpoints.append(
        ConfigurationSetInputEndpoint('ssh', 'tcp', '22', '22'))

    result = sms.create_virtual_machine_deployment(
        service_name=name,
        deployment_name=name,
        deployment_slot='production',
        label=name,
        role_name=name,
        system_config=linux_config,
        os_virtual_hard_disk=vhd,
        network_config=network,
        role_size=INSTANCE_CONFIG['type'])

    print "Hit Ctrl-C when status is Succeded"
    while True:
        status = sms.get_operation_status(result.request_id).status
        print status


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <config-path.json>\n".format(sys.argv[0]))
        sys.exit(1)
    main(*sys.argv[1:])
