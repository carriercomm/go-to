#!/usr/bin/env python

'''
Script to launch Azure VM
'''

__author_ = "Leonid Vasilyev, <vsleonid@gmail.com>"

import json
import hashlib
import time
import os
import sys
import base64
from datetime import datetime

import azure
from azure.servicemanagement import *

INSTANCE_CONFIG = {
    "region": "West Europe",
    "image": "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu_DAILY_BUILD-precise-12_04_3-LTS-amd64-server-20131205-en-us-30GB",
    "type": "Medium",
}


def main(config_path, prefix):
    with open(config_path) as f:
        config = json.load(f)

    name = prefix + "-" + hashlib.md5(datetime.utcnow().isoformat()).hexdigest()

    sms = ServiceManagementService(
        config['subscription_id'],
        config['api_certificate_path'])

    sms.create_hosted_service(
        service_name=name,
        label=name,
        location=INSTANCE_CONFIG['region'])

    cert_data = open(config['certificate_path']).read()
    fingerpring = hashlib.sha1(cert_data).hexdigest().upper()
    sms.add_management_certificate(
        public_key=cert_data,
        thumbprint=fingerpring,
        data=cert_data
    )

    # Try to reuse storage account first
    # becase limit of storage accounts is by default 1.
    storage_accounts = sms.list_storage_accounts()

    if len(storage_accounts):
        storage = storage_accounts[-1]
        # Storage and Service can't be in different regions
        if storage.storage_service_properties.location != INSTANCE_CONFIG["region"]:
            raise ValueError(
                ("Can't use Storage account from different region: service is in"
                 "{} but storage is in {}").format(
                    INSTANCE_CONFIG["region"],
                    storage.storage_service_properties.location))
        storage_name = storage.service_name
    else:
        storage_name = name.replace("-", "")[:24]

        sms.create_storage_account(
            service_name=storage_name,
            description=storage_name,
            label=storage_name,
            location=INSTANCE_CONFIG['region']
        )

    vhd = OSVirtualHardDisk(
        INSTANCE_CONFIG["image"],
        "http://{service}.blob.core.windows.net/{container}/{blob}.vhd".format(
            service=storage_name,
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
        fingerpring,
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

    print result

    while True:
        status = sms.get_operation_status(result.request_id).status
        if status != u"InProgress":
            print status
            break
        time.sleep(1)
        print ".",


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: {} <config-path.json> <name-prefix>\n".format(sys.argv[0]))
        sys.exit(1)
    main(*sys.argv[1:])
