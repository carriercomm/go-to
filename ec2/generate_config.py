#!/usr/bin/env python

'''
Generate config to access AWS Ec2
'''

__author__ = "Leonid Vasilyev, <vsleonid@gmail.com>"

import base64
import json
import os
import subprocess
import sys
import stat

import boto
import boto.ec2


def generate_server_cert(pem, cer):
    if not os.path.exists(pem):
        raise ValueError("{} doesn't exists".format(pem))

    if os.path.exists(cer):
        sys.stderr.write("{} already exists".format(cer))
        return

    cmd = [
        "ssh-keygen",
        "-t",
        "rsa",
        "-y",
        "-f",
        pem
    ]
    with open(cer, "w") as f:
        subprocess.check_call(" ".join(cmd), stdout=f, shell=True)


def generate_client_cert(pem):
    if os.path.exists(pem):
        sys.stderr.write("{} already exists".format(pem))
        return
    cmd = [
        "openssl",
        "genrsa",
        "1024"
    ]
    with open(pem, "w") as f:
        subprocess.check_call(" ".join(cmd), stdout=f, shell=True)

    os.chmod(pem, stat.S_IREAD | stat.S_IWRITE)


def main(key, secret, ssh_key_name, ssh_key_dir, config_path):
    ssh_key_dir = os.path.abspath(ssh_key_dir)

    cer = ssh_key_name + ".cer"
    pem = ssh_key_name + ".pem"

    cer_path = os.path.join(ssh_key_dir, cer)
    pem_path = os.path.join(ssh_key_dir, pem)

    config = {
        "access_key_id": key,
        "secret_access_key": secret,
        "certificate_path": pem_path,
    }

    generate_client_cert(pem_path)
    generate_server_cert(pem_path, cer_path)

    all_regions = boto.ec2.regions(
        aws_access_key_id=key,
        aws_secret_access_key=secret)

    with open(cer_path, 'rb') as f:
        cert_data = f.read()

    for region in all_regions:
        print "---"
        print "Importing to:", region.name
        print "---"
        try:
            ec2 = boto.ec2.connect_to_region(
                region.name,
                aws_access_key_id=key,
                aws_secret_access_key=secret)

            ec2.import_key_pair(
                    ssh_key_name,
                    cert_data)

        except Exception as e:
            sys.stderr.write(
                "Unable to import {} to {}: {}\n".format(
                    ssh_key_name, region.name, e))

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.stderr.write(
            "Usage: {} <aws_key> <aws_secret> <ssh_key_name> <ssh_key_dir> <config_path.json>\n".format(sys.argv[0]))
        sys.exit(1)
    main(*sys.argv[1:])

