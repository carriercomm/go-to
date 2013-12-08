#!/usr/bin/env python

'''
Start new ec2 instance with open ssh port
'''

__author__ = "Leonid Vasilyev, <vsleonid@gmail.com>"

import json
import os
import sys
import time
from datetime import datetime

import boto
import boto.ec2


# based on http://cloud-images.ubuntu.com/releases/precise/release/
INSTANCE_CONFIG = {
    "ami": "ami-14907e63", # Ubuntu 12.04.3 LTS eu-west-1 64-bit instance
    "region": "eu-west-1",
    "type": "m1.small",
}


def main(config_path, name_prefix, tag):
    with open(config_path) as f:
        config = json.load(f)

    ec2 = boto.ec2.connect_to_region(
        INSTANCE_CONFIG['region'],
        aws_access_key_id=config['access_key_id'],
        aws_secret_access_key=config['secret_access_key'])

    name = name_prefix + "-" + datetime.utcnow().isoformat()

    # Assume that ssh key is uploaded

    group = ec2.create_security_group(
        name,
        'A group that allows SSH access')
    group.authorize('tcp', 22, 22, "0.0.0.0/0")

    reservation = ec2.run_instances(
            INSTANCE_CONFIG['ami'],
            key_name=os.path.basename(config['certificate_path']).split(".")[0],
            instance_type=INSTANCE_CONFIG['type'],
            security_groups=[name])

    # Find the actual Instance object inside the Reservation object
    # returned by EC2.

    instance = reservation.instances[0]

    # The instance has been launched but it's not yet up and
    # running.  Let's wait for it's state to change to 'running'.

    print 'waiting for instance'
    while instance.state != 'running':
        print '.',
        time.sleep(1)
        instance.update()
    print 'done'

    instance.add_tag(tag)

    print "DoNe! To connect use:"
    print "ssh -i {} ubuntu@{}".format(
        config['certificate_path'],
        instance.public_dns_name
    )


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write("Usage:\n {} <config-path> <name-prefix> <tag>\n".format(sys.argv[0]))
        sys.exit(1)
    main(*sys.argv[1:])
