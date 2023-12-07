#!/usr/bin/python3

import os
from bots import bots

div = "------------------------------"

for bot in bots:
    os.system('docker exec -it ' + str(bot) + ' /bin/bash -c "pgrep -x redrocket.py"')
    print(div)
