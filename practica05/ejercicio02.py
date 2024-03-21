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
import threading

home = '/home/gfons/Downloads'

def create_media():
    video = vlc.Media(f'{home}/videos/video.mp4')
    pics = []
    for i in range(1,5):
        pics.append(vlc.Media(f'{home}/pictures/pic0{i}.jpg'))
    return video, pics

def play_video(player, video):
    # Load the media into the player
    player.set_media(video)
    # Play the video
    player.play()
    # Let the video play for 10 secs
    time.sleep(10)

def loop_pics(player, pics):
    i = 0
    while True:
        player.set_media(pics[i])
        player.play()
        time.sleep(3)
        i = (i + 1) % len(pics)

# INI: USBDETECT_1
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

def usbdetect() {
    global monitor
    global player
    while True:
        action, device = monitor.receive_device()
        if action != "add":
            continue
        print_dev_info(device)
        auto_mount("/dev/" + device.sys_name)
        mp = get_mount_point("/dev/" + device.sys_name)
        print("Mount point: {}".format(mp))
        print_dev_stats(mp)

        images = [f'{path}/{f}' for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]
        loop_pics(player, images)
}

###### MAIN ######
usbdetect_p = threading.Thread(target=usbdetect)
usbdetect_p.daemon = True
usbdetect_p.start()

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")
# FIN: USBDETECT_1

# Create the player
player = vlc.MediaPlayer()
player.set_fullscreen(True)
# Create the media objects
video, pics = create_media()
# Play video for 10 seconds
play_video(player, video)
 # Play pictures in loop
loop_pics(player, pics)