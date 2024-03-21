#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# usbdetect.py
#
# Author:  Mauricio Matamoros
# Date:    2022.09.13
# License: MIT
#
# Detects when a USB media is inserted and prints the list of images within

import os
import pyudev
import subprocess as sp

def print_dev_stats(path):
    photos = []
    for file in os.listdir(path):
        if file.endswith(".jpg") or file.endswith(".png"):
            photos.append(file)
    print("{} has {} photos.".format(path, len(photos)))

def print_dev_info(device):
    print("Device sys_path: {}".format(device.sys_path))
    print("Device sys_name: {}".format(device.sys_name))
    print("Device sys_number: {}".format(device.sys_number))
    print("Device subsystem: {}".format(device.subsystem))
    print("Device device_type: {}".format(device.device_type))
    print("Device is_initialized: {}".format(device.is_initialized))

def is_mounted(device_path):
    # Check if the device is already mounted
    args = ["findmnt", "-rn", "-o", "SOURCE", "--noheadings", device_path]
    cp = sp.run(args, capture_output=True, text=True)
    return cp.returncode == 0

def auto_mount(device_path):
    # Mount the device if it's not already mounted
    if not is_mounted(device_path):
        args = ["udisksctl", "mount", "-b", device_path]
        sp.run(args)

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")
while True:
    action, device = monitor.receive_device()
    if action != "add":
        continue
    print_dev_info(device)
    device_path = "/dev/" + device.sys_name
    print("Device path: {}".format(device_path))
    auto_mount(device_path)
    mp = get_mount_point(device_path)
    print("Mount point: {}".format(mp))
    print_dev_stats(mp)
    break
