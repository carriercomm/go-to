#!/usr/bin/env python

'''
Generate config to access AWS Ec2
'''

import sys
import os
import json

import boto


def main(key, secret, ssh_key_name, ssh_key_path, config_path):
    config = {
        "access_key_id": key,
        "secret_access_key": secret 
    }

    # TODO:
    # Create an SSH key to use when logging into instances. key =
    # ec2.create_key_pair(key_name)
    # AWS will store the public key but the private key is
    # generated and returned and needs to be stored locally. # The save method
    # will also chmod the file to protect
    # your private key.
    # key.save(key_dir)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write(
            "Usage: {} <aws_key> <aws_secret> <ssh_key_name> <ssh_key_path> <config_path.json>\n".format(sys.argv[0]))
        sys.exit(1)
    main(*sys.argv[1:])

