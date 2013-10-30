#!/usr/bin/env python

'''
Check Ec2 configuration
'''

import sys
import json

import boto.ec2
import boto.exception


def main(config_path):
    config = {}
    with open(config_path) as f:
        config = json.load(f)

    regions = boto.ec2.regions(
        aws_access_key_id=config['access_key_id'],
        aws_secret_access_key=config['secret_access_key']
    )

    print "Ec2 regions:"
    print "-----------"

    for r in sorted(regions, key=lambda o: o.name):
        print "{: <20} https://{}".format(r.name, r.endpoint)

    print ""
    print "Ec2 reservations:"
    print "----------------"

    for reg in regions:
        print ""
        print "Reservaions for {}:".format(reg.name)
        conn = boto.ec2.connect_to_region(
            reg.name,
            aws_access_key_id=config['access_key_id'],
            aws_secret_access_key=config['secret_access_key'])
        try:
            print "\n".join(
                "  * id:{}\n    owner_id:{}\n    instasnces: {}".format(
                    r.id, r.owner_id,
                    ",".join([i.public_dns_name for i in r.instances]))
                for r in conn.get_all_reservations())
        except boto.exception.EC2ResponseError:
            pass

        print ""
        print "  Available keypairs:"
        print "  =================="

        try:
            for keypair in conn.get_all_key_pairs():
                print "   -" + keypair.name
        except boto.exception.EC2ResponseError:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <config.json>\n".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
