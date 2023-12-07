#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


# import proxies as list
with open('bots.txt', 'r') as f:
    bots = [line for line in f.read().splitlines() if line.strip()]


div = "------------------------------"

for bot in bots:
    os.system('docker exec -it ' + str(bot) + ' /bin/bash -c "tail -n 10 redrocket.log"')
    print(div)
