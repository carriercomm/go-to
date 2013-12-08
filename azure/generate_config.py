#!/usr/bin/env python

'''
Generate config for Azure
'''

__author__ = "Leonid Vasilyev, <vsleonid@gmail.com>"


import sys
import os
import subprocess
import json


def generate_server_cert(pem, cer):
    if not os.path.exists(pem):
        raise ValueError("{} doesn't exists".format(pem))

    if os.path.exists(cer):
        sys.stderr.write("{} already exists".format(cer))
        return

    cmd = [
        "openssl",
        "x509",
        "-inform",
        "pem",
        "-in",
        pem,
        "-outform",
        "der",
        "-out",
        cer,
    ]
    subprocess.check_call(" ".join(cmd), shell=True)


def generate_client_cert(pem):
    if os.path.exists(pem):
        sys.stderr.write("{} already exists".format(pem))
        return
    cmd = [
        "openssl",
        "req",
        "-x509",
        "-nodes",
        "-days",
        "365",
        "-newkey",
        "rsa:1024",
        "-keyout",
        pem,
        "-out",
        pem,
    ]
    subprocess.check_call(" ".join(cmd), shell=True)


def main(subscription_id, cert_path, config_path):
    if os.path.exists(config_path):
        raise ValueError("{} exists".format(config_path))

    cer = cert_path + ".cer"
    pem = cert_path + ".pem"

    generate_client_cert(pem)
    generate_server_cert(pem, cer)

    config = {}
    config['subscription_id'] = subscription_id
    config['certificate_path'] = pem

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write(
            "Usage: {} <subscription_id> <cert_path> <config-name.json>\n".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
