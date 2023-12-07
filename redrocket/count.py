#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re


with open(r'redrocket.log', 'r') as f:
    log_file = f.read().splitlines()


c = 0
for line in log_file:
    # this will not match for passed video (which were likely watched)
    if re.search(r'current video:', line):
        c += 1


print(str(c))
