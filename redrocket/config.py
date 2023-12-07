#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import random
import logging

# Sentry logging
# import sentry_sdk as sentry
# sentry.init("https://6e9a5d201ca547e99d41e21536f24a8d@sentry.io/3106807")

# set home directory path variable
# homedir = os.path.expanduser('~')
homedir = './'

# TODO for dynamic logging
node_id = 'node_x'

# logging handler
logging.basicConfig(filename=homedir + '/redrocket.log',
    filemode='a+',
    format=node_id + ' %(asctime)s %(levelname)-8s "%(message)s"',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M')

# import proxies as list
with open('proxies.txt', 'r') as f:
    proxies = [line for line in f.read().splitlines() if line.strip()]

# import playlists as list
with open('playlists.txt', 'r') as f:
    playlists = [line for line in f.read().splitlines() if line.strip()]


# shuffle proxies and playlists
random.shuffle(proxies)
random.shuffle(playlists)
