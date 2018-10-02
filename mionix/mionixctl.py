#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import mionix
import yaml
import argparse
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description="Mionix Avior 7000 configuration utility")
    subparsers = parser.add_subparsers(help="commands", dest="command")
    save_parser = subparsers.add_parser('upload', help="upload a profile to the mouse")
    save_parser.add_argument("num", help="number of profile")
    save_parser.add_argument("profilefile", help="filename of the profile")
    save_parser.add_argument("--activate", "-a", action="store_true", help="apply the saved profile")
    cdefault_parser = subparsers.add_parser("create_default", help="Create a default profile and write it to a file")
    cdefault_parser.add_argument("filename", type=str, help="filename to write to")
    apply_parser = subparsers.add_parser("activate", help="activate a profile")
    apply_parser.add_argument("num", help="number of profile")
    subparsers.add_parser("find_device", help="find and print the hidraw device")

    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    return args


def handle_command(args):
    if args.command == "find_device":
        dev = mionix.find_device_path(mionix.MIONIX_AVIOR_7000_USB_ID, mionix.MIONIX_AVIOR_7000_USB_INTERFACE_NUM)
        print("device: {}".format(dev))
        return
    elif args.command == "create_default":
        print("writing default profile to file {}".format(args.filename))
        p = mionix.Avior7000SerializableProfile()
        with open(args.filename, "w") as f:
            f.write(yaml.dump(p))
    elif args.command == "upload":
        num = int(args.num)
        filename = args.profilefile
        print("Loading profile %s" % filename)
        with open(filename) as f:
            text = f.read()
        print("will write profile to place {}".format(num))
        device = mionix.Avior7000()
        device.set_apply_profile(text, num)
        if args.activate:
            time.sleep(0.1)
            print("Activating profile {}".format(num))
            device.apply_profile(num)
    elif args.command == "activate":
        num = int(args.num)
        device = mionix.Avior7000()
        print("Activating profile {}".format(num))
        device.apply_profile(num)


def main():
    args = parse_arguments()
    handle_command(args)
    return 0


if __name__ == "__main__":
    main()
