#!/usr/bin/env python

'''
Check access to Azure API
'''

__author__ = "Leonid Vasilyev, <vsleonid@gmail.com>"


import json
import sys
import os


import azure.servicemanagement as smgmt


def print_locations_and_services(sms):
    print "Available locations & services:"
    print "=============================="

    for i, loc in enumerate(sms.list_locations()):
        print("{}.{}:\n  {}".format(
            i + 1,
            loc.display_name,
            ", ".join(loc.available_services)))


def print_available_os_images(sms):
    print "Available OS images:"
    print "==================="

    def _by_os_and_label(image):
        return image.os, image.label

    for image in sorted(sms.list_os_images(), key=_by_os_and_label):
        print "{os}: {label} ({size}GB)\n{name}".format(
            os=image.os,
            label=image.label,
            size=image.logical_size_in_gb,
            name=image.name
        )
        print " "


def print_disks_info(sms):
    print "Disks info:"
    print "=========="

    for disk in sms.list_disks():
        print "{name}({size}GB):\n{source}\n{attached}".format(
            name=disk.name,
            size=disk.logical_disk_size_in_gb,
            source=disk.source_image_name,
            attached=disk.attached_to.hosted_service_name +
            "/" + disk.attached_to.deployment_name
        )
        print " "


def print_hosted_services(sms):
    print "Hosted Services Info:"
    print "===================="
    for service in sms.list_hosted_services():
        print service.service_name
        for k, v in service.hosted_service_properties.__dict__.iteritems():
            if k.startswith('_'):
                continue
            print "  {}: {}".format(k, v)


def main(config_path):
    if not os.path.exists(config_path):
        raise ValueError("'{}' doesn't exists".format(config_path))

    config = {}
    with open(config_path) as f:
        config = json.load(f)

    subscription_id = config['subscription_id']
    certificate_path = config['certificate_path']

    sms = smgmt.ServiceManagementService(subscription_id, certificate_path)

    print "Account summary:"
    print "---------------"
    print_locations_and_services(sms)
    print_available_os_images(sms)
    print_disks_info(sms)
    print_hosted_services(sms)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write(
            "Usage: {} <config-file.json>\n".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
