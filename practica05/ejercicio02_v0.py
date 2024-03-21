#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# kyosk.py
#
# Author:  Mauricio Matamoros
# Date:    2023.02.14
# License: MIT
#
# Plays a set of files using VLC with the Raspberry Pi
#

import os
import pyudev
import vlc
import time
import subprocess as sp

home = '/home/pi'

def create_media():
    video = vlc.Media(f'{home}/videos/video.mp4')
    return video

def play_video(player, video):
    # Load the media into the player
    player.set_media(video)

    # Play the video
    player.play()

    # Slowly increase volume
    for i in range(101):
        player.audio_set_volume(i)
        time.sleep(0.1)
    # Let the video play for 10 secs
    time.sleep(10)
    # Slowly decrease volume
    for i in range(100, -1, -1):
        player.audio_set_volume(i)
        time.sleep(0.1)

def play_images(player, path):
    images = [f'{path}/{f}' for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]
    while True:
        for image in images:
            player.set_media(vlc.Media(image))
            player.play()
            time.sleep(3)

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

def auto_mount(path):
    args = ["udisksctl", "mount", "-b", path]
    sp.run(args)

def get_mount_point(path):
    args = ["findmnt", "-unl", "-S", path]
    cp = sp.run(args, capture_output=True, text=True)
    out = cp.stdout.split(" ")[0]
    return out

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")
player = vlc.MediaPlayer()
player.set_fullscreen(True)

video = create_media()
play_video(player, video)

while True:
    action, device = monitor.receive_device()
    if action != "add":
        continue
    print_dev_info(device)
    auto_mount("/dev/" + device.sys_name)
    mp = get_mount_point("/dev/" + device.sys_name)
    print("Mount point: {}".format(mp))
    print_dev_stats(mp)
    play_images(player, mp)
